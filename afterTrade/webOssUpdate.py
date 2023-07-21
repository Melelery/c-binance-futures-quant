#!/usr/bin/python3.10
# encoding:utf-8
import time
import requests
import json
import random
import traceback
import _thread
from config import *
from commonFunction import FunctionClient

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="dataToOss",connectMysql =True)

DAY_INCOME_TABLE_NAME = "income_history_take_day"

INCOME_TABLE_NAME = "income_history_take"

INIT_DAY_INCOME_RECORD_TIME = "2023-07-20 00:00:00"


tableName = DAY_INCOME_TABLE_NAME
tableExit = False
sql ="show tables;"
tableData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tableData)):
    if tableData[a][0]==tableName:
        tableExit = True

if not tableExit:
    sql="""CREATE TABLE `"""+tableName+"""` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dayBeginTime` varchar(30) DEFAULT NULL,
  `dayEndTime` varchar(30) DEFAULT NULL,
  `commission` double(30,10) DEFAULT NULL,
  `profit` double(30,10) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
;
"""
    FUNCTION_CLIENT.mysql_commit(sql,[])

LAST_GENERATE_TIME = ""

HISTORY_INVESTOR_OBJ = [
    {
        "id":1,
        "beginTime":"2023-05-09",
        "endTime":"2023-05-28",
        "initValue":0,
        "endValue":0,
        "userData":[]

    }
]
INVESTOR_OBJ =[{'name': 'mele', 'time': '2023-07-20 00:00:00', 'percent': 100, 'initValue': 922, 'assetsWhileJoin': 922, 'protectValue': 0}]



PROFIT_UPDATE_TS = 0

INFO_OBJ = {}



def getProfit():
    global ALL_PROFIT,MAKER_COMMISSION_RATE,FUNCTION_CLIENT,INCOME_TABLE_NAME,INFO_OBJ,PROFIT_UPDATE_TS,SEND_PROFIT_EX_TS
    now = int(time.time()*1000)
    todayTs = FUNCTION_CLIENT.turn_ts_to_time(FUNCTION_CLIENT.turn_ts_to_day_time(int(time.time())))*1000

    nowMin = int(FUNCTION_CLIENT.turn_ts_to_min(now))
    print(nowMin)
    if (todayTs != PROFIT_UPDATE_TS and nowMin>=5) or INFO_OBJ=={}:

        sql = "select income,binance_ts,incomeType,bnbPrice,asset,symbol from income_history_take where binance_ts<%s"
        data = FUNCTION_CLIENT.mysql_select(sql,[todayTs])
        INFO_OBJ["p"] = {}
        INFO_OBJ["c"] = {}
        INFO_OBJ["v"] = {}
        INFO_OBJ["t"] = 0
        for i in range(len(data)):
            income = data[i][0]
            binanceTs = data[i][1]
            incomeType = data[i][2]
            bnbPrice = data[i][3]
            asset = data[i][4]
            symbol = data[i][5]

            if symbol!='':
                realIncome = 0
                if not (symbol in INFO_OBJ["p"]):
                    INFO_OBJ["p"][symbol]=[0,0,0,0]
                if not (symbol in INFO_OBJ["c"]):
                    INFO_OBJ["c"][symbol]=[0,0,0,0]
                if not (symbol in INFO_OBJ["v"]):
                    INFO_OBJ["v"][symbol]=[0,0,0,0]

                if asset=="BNB":
                    realIncome = income*bnbPrice
                else:
                    realIncome = income
                if incomeType=="COMMISSION":
                    if binanceTs>=todayTs-86400*1000:
                        INFO_OBJ["c"][symbol][0] = INFO_OBJ["c"][symbol][0]+realIncome*0.6
                        if asset=="BNB":
                            INFO_OBJ["v"][symbol][0] = INFO_OBJ["v"][symbol][0]+income*0.6

                    if binanceTs>=todayTs-7*24*60*60*1000:
                        INFO_OBJ["c"][symbol][1] = INFO_OBJ["c"][symbol][1]+realIncome*0.6
                        if asset=="BNB":
                            INFO_OBJ["v"][symbol][1] = INFO_OBJ["v"][symbol][1]+income*0.6
                    if binanceTs>=todayTs-30*24*60*60*1000:
                        INFO_OBJ["c"][symbol][2] = INFO_OBJ["c"][symbol][2]+realIncome*0.6
                        if asset=="BNB":
                            INFO_OBJ["v"][symbol][2] = INFO_OBJ["v"][symbol][2]+income*0.6

                    INFO_OBJ["c"][symbol][3] = INFO_OBJ["c"][symbol][3]+realIncome*0.6
                    if asset=="BNB":
                        INFO_OBJ["v"][symbol][3] = INFO_OBJ["v"][symbol][3]+income*0.6

                if incomeType=="REALIZED_PNL"  or incomeType=="FUNDING_FEE" :
                    if binanceTs>=todayTs-86400*1000:
                        INFO_OBJ["p"][symbol][0] = INFO_OBJ["p"][symbol][0]+realIncome
                    if binanceTs>=todayTs-7*24*60*60*1000:
                        INFO_OBJ["p"][symbol][1] = INFO_OBJ["p"][symbol][1]+realIncome
                    if binanceTs>=todayTs-30*24*60*60*1000:
                        INFO_OBJ["p"][symbol][2] = INFO_OBJ["p"][symbol][2]+realIncome

                    INFO_OBJ["p"][symbol][3] = INFO_OBJ["p"][symbol][3]+realIncome
                if  incomeType=="COMMISSION":
                    if binanceTs>=todayTs-86400*1000:
                        INFO_OBJ["p"][symbol][0] = INFO_OBJ["p"][symbol][0]+realIncome*0.6
                    if binanceTs>=todayTs-7*24*60*60*1000:
                        INFO_OBJ["p"][symbol][1] = INFO_OBJ["p"][symbol][1]+realIncome*0.6
                    if binanceTs>=todayTs-30*24*60*60*1000:
                        INFO_OBJ["p"][symbol][2] = INFO_OBJ["p"][symbol][2]+realIncome*0.6

                    INFO_OBJ["p"][symbol][3] = INFO_OBJ["p"][symbol][3]+realIncome*0.6
        INFO_OBJ["p"]["all"] = [0,0,0,0]
        for key in (INFO_OBJ["p"]):
            for i in range(4):
                if key!="all":
                    INFO_OBJ["p"]["all"][i] = INFO_OBJ["p"]["all"][i]+INFO_OBJ["p"][key][i]
                INFO_OBJ["p"][key][i] = INFO_OBJ["p"][key][i]

        INFO_OBJ["v"]["all"] = [0,0,0,0]
        for key in (INFO_OBJ["v"]):
            for i in range(4):
                if key!="all":
                    INFO_OBJ["v"]["all"][i] = INFO_OBJ["v"]["all"][i]+INFO_OBJ["v"][key][i]
                INFO_OBJ["v"][key][i] = INFO_OBJ["v"][key][i]

        INFO_OBJ["c"]["all"] = [0,0,0,0]
        for key in (INFO_OBJ["c"]):
            for i in range(4):
                if key!="all":
                    INFO_OBJ["c"]["all"][i] = INFO_OBJ["c"]["all"][i]+INFO_OBJ["c"][key][i]
                INFO_OBJ["c"][key][i] = INFO_OBJ["c"][key][i]

        INFO_OBJ["t"] = todayTs
        PROFIT_UPDATE_TS = todayTs
        # except Exception as e:
        #     print(e)
        #     FUNCTION_CLIENT.send_lark_msg_limit_one_min("getProfit ex:"+str(e))


POSITION_ARR = []

ACCOUNT_BALANCE_VALUE = 0

def getBinancePositionFromMyServer():
    global FUNCTION_CLIENT,POSITION_ARR,ACCOUNT_BALANCE_VALUE
    try:
        dataStr = FUNCTION_CLIENT.get_from_ws_a("B")
        dataArr = dataStr.split("*")
        ACCOUNT_BALANCE_VALUE = float(dataArr[4])
        if dataArr[2]!="":
            positionStrArr= dataArr[2].split("&")
            positionArr= []
            for a in range(len(positionStrArr)):
                positionArr.append(positionStrArr[a].split("@"))
                positionArr[a][1] = float(positionArr[a][1])
                positionArr[a][2] = float(positionArr[a][2])
            POSITION_ARR = positionArr
        else:
            POSITION_ARR = []
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))


def getPositionInfoArrBySymbol(symbol):
    global POSITION_ARR
    for positionIndex in range(len(POSITION_ARR)):
        if POSITION_ARR[positionIndex][0] == symbol:
            return [POSITION_ARR[positionIndex][2],POSITION_ARR[positionIndex][1]]
    return [0,0]


SECOND_OPEN_OBJ_ARR = []

SECOND_OPEN_OBJ_ARR_UPDATE_TS = 0

SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME = random.randint(1,60)

TODAY_PROFIT = 0

LAST_GENERATE_TS = 0

def generateObj():
    global POSITION_ARR,ACCOUNT_BALANCE_VALUE,LAST_GENERATE_TS,TODAY_PROFIT,MAKER_COMMISSION_RATE,TAKER_COMMISSION_RATE,INFO_OBJ,FUNCTION_CLIENT,LAST_GENERATE_TIME,INVESTOR_OBJ,HISTORY_INVESTOR_OBJ,SECOND_OPEN_OBJ_ARR,SECOND_OPEN_OBJ_ARR_UPDATE_TS,SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME
    nowTime = FUNCTION_CLIENT.turn_ts_to_time(int(time.time()))
    now = int(time.time()*1000)
    if now - LAST_GENERATE_TS>3000:

        LAST_GENERATE_TS = now

        sql = "select `status`,`update_ts`,`run_time` from trade_machine_status order by update_ts asc"
        TRADE_MACHINE_STATUS_DATA = FUNCTION_CLIENT.mysql_select(sql,[])

        allRunTime = 0
        for i in range(len(TRADE_MACHINE_STATUS_DATA)):
            allRunTime = allRunTime+TRADE_MACHINE_STATUS_DATA[i][2]

        systemAverageRunTime = int(allRunTime/len(TRADE_MACHINE_STATUS_DATA))
        systemUpdateTs = TRADE_MACHINE_STATUS_DATA[0][1]
        systemStatus = TRADE_MACHINE_STATUS_DATA[0][0]


        bigLossTradeArr = []
        sql = "select `symbol`,`endTs`,`profit`,`profitPercentByBalance`,extraInfo,direction from trades_take where status='updateProfit' order by id asc limit 1000"
        bigLossData = FUNCTION_CLIENT.mysql_select(sql,[])

        for i in range(len(bigLossData)):
            extraInfo = json.loads(bigLossData[i][4])
            priceRate = 0
            if "priceRate" in extraInfo:
                priceRate = abs(int(float(extraInfo["priceRate"])*100)/100)
            bigLossTradeArr.insert(0,[
                    bigLossData[i][0],
                    FUNCTION_CLIENT.turn_ts_to_time(bigLossData[i][1]),
                    int(bigLossData[i][2]),
                    str(abs(int(bigLossData[i][3]*100)/100))+"%",
                    priceRate,
                    bigLossData[i][5]
                ])


        getBinancePositionFromMyServer()

        allPositionValue = 0
        positionArr = []
        for a in range(len(POSITION_ARR)):
            positionValue = int(abs(float(POSITION_ARR[a][1])*float(POSITION_ARR[a][2])))
            allPositionValue = allPositionValue + positionValue
            direction = "s"
            if float(POSITION_ARR[a][1])>0:
                direction = "l"
            positionArr.append({
                    "value":positionValue,
                    "symbol":float(POSITION_ARR[a][0]),
                    "direction":direction,
                    "entryPrice":float(POSITION_ARR[a][2])
                })

        # for key in result["profit"]:
        #     for keyT in result["profit"][key]:
        #         result["profit"][key][keyT] = int(result["profit"][key][keyT])


        # secondOpenObjArr = {"profit":result["profit"],"commission":result["commission"]}

        # if now - SECOND_OPEN_OBJ_ARR_UPDATE_TS>60000*SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME:
        #     SECOND_OPEN_OBJ_ARR = secondOpenObjArr
        #     SECOND_OPEN_OBJ_ARR_UPDATE_TS = now
        #     SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME = random.randint(1,60)

        todayTs = FUNCTION_CLIENT.turn_ts_to_time(FUNCTION_CLIENT.turn_ts_to_day_time(int(time.time())))*1000

        sql = "select income,binance_ts,incomeType,bnbPrice,asset,symbol from income_history_take where binance_ts>=%s"
        incomeData = FUNCTION_CLIENT.mysql_select(sql,[now-86400000])
        oneDayVol = 0
        oneDayProfit = 0
        todayProfit = 0
        for i in range(len(incomeData)):
            income = incomeData[i][0]
            binanceTs = incomeData[i][1]
            incomeType = incomeData[i][2]
            bnbPrice = incomeData[i][3]
            asset = incomeData[i][4]
            symbol = incomeData[i][5]

            if symbol!='':
                realIncome = 0
                if not (symbol in INFO_OBJ["p"]):
                    INFO_OBJ["p"][symbol]=[0,0,0,0]
                if not (symbol in INFO_OBJ["c"]):
                    INFO_OBJ["c"][symbol]=[0,0,0,0]
                if not (symbol in INFO_OBJ["v"]):
                    INFO_OBJ["v"][symbol]=[0,0,0,0]

                if asset=="BNB":
                    realIncome = income*bnbPrice
                else:
                    realIncome = income

                if incomeType=="COMMISSION":

                    if realIncome>0:
                        oneDayVol = oneDayVol+realIncome*0.6
                    else:
                        oneDayVol = oneDayVol+realIncome*0.6


                if incomeType=="REALIZED_PNL" or incomeType=="FUNDING_FEE":
                    oneDayProfit = oneDayProfit+realIncome
                    if binanceTs>=todayTs:
                        todayProfit = todayProfit+realIncome
                if incomeType=="COMMISSION":
                    oneDayProfit = oneDayProfit+realIncome*0.6
                    if binanceTs>=todayTs:
                        todayProfit = todayProfit+realIncome*0.6



        fromLastInvestor = []
        lastOneDays = []
        lastSevenDays = []
        lastOneMonth = []
        TODAY_PROFIT = todayProfit


        pushObj = {
            "positionArr":positionArr,
            "todayProfit":todayProfit,
            "oneDayVol":int(abs(oneDayVol)),
            "oneDayProfit":int(oneDayProfit),
            "allPositionValue":int(allPositionValue),
            "secondOpenObjArr":INFO_OBJ,
            "accountBalanceValue":ACCOUNT_BALANCE_VALUE,
            "bigLossTradeArr":bigLossTradeArr,
            "investPercentObjArr":INVESTOR_OBJ,
            "systemStatus":systemStatus,
            "systemUpdateTs":systemUpdateTs,
            "runTime":allRunTime,
        }

        LAST_GENERATE_TIME = nowTime
        FUNCTION_CLIENT.oss_put_obj(pushObj,"cQuant/"+nowTime+".json")

        FUNCTION_CLIENT.oss_put_obj(pushObj,"cQuant/a.json")

        pushObj = {
            "now":INVESTOR_OBJ,
            "history":HISTORY_INVESTOR_OBJ
        }
        FUNCTION_CLIENT.oss_put_obj(pushObj,"investor/"+nowTime+".json")
    time.sleep(1)


LAST_UPDATE_RECORD_TIME = ""
def updateRecord():
    global INVESTOR_OBJ,LAST_UPDATE_RECORD_TIME
    nowTime = FUNCTION_CLIENT.turn_ts_to_time(int(time.time()))
    if LAST_UPDATE_RECORD_TIME!=nowTime:
        LAST_UPDATE_RECORD_TIME = nowTime
        now  = int(time.time())
        sql = "select `positionValue`,`balance`,`ts`,`time` from position_record order by id asc"
        positionRecordData = FUNCTION_CLIENT.mysql_select(sql,[])

        fromLastInvestorLimitTs = FUNCTION_CLIENT.turn_ts_to_day_time(INVESTOR_OBJ[0]["time"])
        # fromLastInvestorLimitTs = FUNCTION_CLIENT.turn_ts_to_day_time('2023-06-13 20:17:00')
        print("fromLastInvestorLimitTs:"+str(fromLastInvestorLimitTs))
        lastOneDayLimitTs = now-86400
        lastSevenDaysLimitTs = now-7*86400
        lastOneMonthLimitTs = now-30*86400


        fromLastInvestorArr = []
        lastDataTsA = 0
        lastBalanceA = 0
        lastPositionValueA = 0

        lastOneDayArr = []
        lastDataTsB = 0
        lastBalanceB = 0
        lastPositionValueB = 0

        lastSevenDaysArr = []
        lastDataTsC = 0
        lastBalanceC = 0
        lastPositionValueC = 0

        lastOneMonthArr = []
        lastDataTsD = 0
        lastBalanceD = 0
        lastPositionValueD = 0

        allArr = []
        lastDataTsE = 0
        lastBalanceE = 0
        lastPositionValueE = 0

        for i in range(len(positionRecordData)):
            dataTs = positionRecordData[i][2]
            positionValue =  int(positionRecordData[i][0])
            balance =  int(positionRecordData[i][1])
            dataTime = positionRecordData[i][3]



            if dataTs>=fromLastInvestorLimitTs:
                tsChange = int(dataTs-lastDataTsA)
                positionValueChange = int(positionValue-lastPositionValueA)
                balanceChange = int(balance-lastBalanceA)
                fromLastInvestorArr.append([positionValueChange,balanceChange,tsChange])
                lastDataTsA = dataTs
                lastPositionValueA = int(positionValue)
                lastBalanceA = int(balance)
            if dataTs>=lastOneDayLimitTs:
                tsChange = int(dataTs-lastDataTsB)
                positionValueChange = int(positionValue-lastPositionValueB)
                balanceChange = int(balance-lastBalanceB)
                lastOneDayArr.append([positionValueChange,balanceChange,tsChange])
                lastDataTsB = dataTs
                lastPositionValueB = int(positionValue)
                lastBalanceB = int(balance)
            if dataTs>=lastSevenDaysLimitTs:
                tsChange = int(dataTs-lastDataTsC)
                positionValueChange = int(positionValue-lastPositionValueC)
                balanceChange = int(balance-lastBalanceC)
                lastSevenDaysArr.append([positionValueChange,balanceChange,tsChange])
                lastDataTsC = dataTs
                lastPositionValueC = int(positionValue)
                lastBalanceC = int(balance)
            if dataTs>=lastOneMonthLimitTs:
                tsDhange = int(dataTs-lastDataTsD)
                positionValueDhange = int(positionValue-lastPositionValueD)
                balanceDhange = int(balance-lastBalanceD)
                lastOneMonthArr.append([positionValueDhange,balanceDhange,tsDhange])
                lastDataTsD = dataTs
                lastPositionValueD = int(positionValue)
                lastBalanceD = int(balance)
            tsEhange = int(dataTs-lastDataTsE)
            positionValueEhange = int(positionValue-lastPositionValueE)
            balanceEhange = int(balance-lastBalanceE)
            allArr.append([positionValueEhange,balanceEhange,tsEhange])
            lastDataTsE = dataTs
            lastPositionValueE = int(positionValue)
            lastBalanceE = int(balance)
        FUNCTION_CLIENT.oss_put_obj(fromLastInvestorArr,"cQuant_change/fromLastInvestorArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastOneDayArr,"cQuant_change/lastOneDayArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastSevenDaysArr,"cQuant_change/lastSevenDaysArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastOneMonthArr,"cQuant_change/lastOneMonthArr.json")
        FUNCTION_CLIENT.oss_put_obj(allArr,"cQuant_change/allArr.json")

UPDATE_DAY_INCOME_TS = 0

def updateDayIncome():
    global UPDATE_DAY_INCOME_TS,TODAY_PROFIT,INIT_DAY_INCOME_RECORD_TIME
    print("update_day_income")
    now = int(time.time())
    if now - UPDATE_DAY_INCOME_TS>60*15:
        UPDATE_DAY_INCOME_TS = now
        incomeDayTableName = DAY_INCOME_TABLE_NAME
        incomeTableName = INCOME_TABLE_NAME
        sql = "select `dayBeginTime` from "+incomeDayTableName+" order by id desc limit 1"
        lastBinanceTsData = FUNCTION_CLIENT.mysql_select(sql,[])

        initIncomeDayTs = FUNCTION_CLIENT.turn_ts_to_time(INIT_DAY_INCOME_RECORD_TIME)
        lastIncomeDayTs = 0
        if len(lastBinanceTsData)>0:
            lastIncomeDayTs = FUNCTION_CLIENT.turn_ts_to_time(lastBinanceTsData[0][0]) 
        if lastIncomeDayTs==0:
            lastIncomeDayTs= initIncomeDayTs
        nowTs = int(time.time())
        todayTs = FUNCTION_CLIENT.turn_ts_to_time(FUNCTION_CLIENT.turn_ts_to_day_time(int(time.time())))

        needInsertDay = int((todayTs - lastIncomeDayTs) /86400)

        for i in range(needInsertDay):
            endDayTs = lastIncomeDayTs+86400*(i+1)
            beginDayTs = lastIncomeDayTs+86400*i
            sql = "select `incomeType`,`income`,`asset`,`bnbPrice` from "+incomeTableName+" where binance_ts>%s and binance_ts<=%s"
            incomeData = FUNCTION_CLIENT.mysql_select(sql,[beginDayTs*1000,endDayTs*1000])

            dayCommission = 0
            dayProfit = 0
            for incomeDataIndex in range(len(incomeData)):
                incomeType = incomeData[incomeDataIndex][0]
                if incomeType=="COMMISSION":
                    if incomeData[incomeDataIndex][2]=="BNB":
                        dayCommission = dayCommission+incomeData[incomeDataIndex][1]*incomeData[incomeDataIndex][3]
                    elif incomeData[incomeDataIndex][2]=="USDT" or incomeData[incomeDataIndex][2]=="BUSD":
                        dayCommission = dayCommission+incomeData[incomeDataIndex][1]
                if incomeType=="REALIZED_PNL" or incomeType=="FUNDING_FEE":
                    if incomeData[incomeDataIndex][2]=="BNB":
                        dayProfit = dayProfit+incomeData[incomeDataIndex][1]*incomeData[incomeDataIndex][3]
                    elif incomeData[incomeDataIndex][2]=="USDT" or incomeData[incomeDataIndex][2]=="BUSD":
                        dayProfit = dayProfit+incomeData[incomeDataIndex][1]
                if incomeType=="COMMISSION" :
                    if incomeData[incomeDataIndex][2]=="BNB":
                        dayProfit = dayProfit+incomeData[incomeDataIndex][1]*incomeData[incomeDataIndex][3]*0.6
                    elif incomeData[incomeDataIndex][2]=="USDT" or incomeData[incomeDataIndex][2]=="BUSD":
                        dayProfit = dayProfit+incomeData[incomeDataIndex][1]*0.6
            print(FUNCTION_CLIENT.turn_ts_to_time(beginDayTs))
            sql = "select `id` from "+incomeDayTableName+" where dayBeginTime=%s"
            incomeData = FUNCTION_CLIENT.mysql_select(sql,[FUNCTION_CLIENT.turn_ts_to_time(beginDayTs)])
            if len(incomeData)==0:
                sql = "INSERT INTO "+incomeDayTableName+" (`dayBeginTime`, `dayEndTime`,`commission`,`profit`)  VALUES (%s,%s,%s,%s);" 
                FUNCTION_CLIENT.mysql_commit(sql,[FUNCTION_CLIENT.turn_ts_to_time(beginDayTs),FUNCTION_CLIENT.turn_ts_to_time(endDayTs),dayCommission,dayProfit])
            else:
                sql = "update "+incomeDayTableName+" set `commission`=%s,`profit`=%s where `dayEndTime`=%s " 
                FUNCTION_CLIENT.mysql_commit(sql,[dayCommission,dayProfit,FUNCTION_CLIENT.turn_ts_to_time(endDayTs)])
        sql = "select `dayBeginTime`,`profit` from "+incomeDayTableName+" order by id asc"
        incomeDayData = FUNCTION_CLIENT.mysql_select(sql,[])
        dayIncomeArr = []
        for i in range(len(incomeDayData)):
            dayIncomeArr.append([incomeDayData[i][0],incomeDayData[i][1]])
        dayIncomeArr.append([ FUNCTION_CLIENT.turn_ts_to_time(todayTs),TODAY_PROFIT])

        ossObj = {
            "ts":int(time.time()),
            "data":dayIncomeArr,
        }
        FUNCTION_CLIENT.oss_put_obj(ossObj,"cQuant_day_income/data.json")


getBinancePositionFromMyServer()
while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        getProfit()
        generateObj()
        updateRecord()
        updateDayIncome()
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(1)
