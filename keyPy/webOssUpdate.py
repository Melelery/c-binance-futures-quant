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

LAST_GENERATE_TIME = ""

HISTORY_INVESTOR_OBJ = [
    {
        "id":1,
        "beginTime":"2023-05-09",
        "endTime":"2023-05-28",
        "initValue":21150,
        "endValue":21180.85,
        "userData":[
            {'name': '吴钊庆', 'time': '2023-05-19 14:59:00', 'initValue': 2800, "userPeriodProfit":-198.5,"profit":-198.5,"userPeriodAnnualized":"-242.85%","techPercent":"0%","periodAnnualized":"-242.85%"}, 
            {'name': '一零二四', 'time': '2023-05-19 13:36:00',  'initValue': 5000, "userPeriodProfit":-351.36,"profit":-351.36,"userPeriodAnnualized":"-239.07%","techPercent":"0%","periodAnnualized":"-239.07%"},
            {'name': '李', 'time': '2023-05-16 21:52:00', 'initValue': 2600, "userPeriodProfit":-127.94,"profit":-127.94,"userPeriodAnnualized":"-166.34%","techPercent":"0%","periodAnnualized":"-166.34%"}, 
            {'name': 'michael', 'time': '2023-05-12 20:28:00',  'initValue': 10000,  "userPeriodProfit":335.316,"profit":1117.72,"userPeriodAnnualized":"241.04%","techPercent":"70%","periodAnnualized":"-39.73%"}, 
            {'name': 'ming', 'time': '2023-05-09 00:00:00',  'initValue': 750, "userPeriodProfit":72.6654,"profit":242.218,"userPeriodAnnualized":"737.79%","techPercent":"70%","periodAnnualized":"-39.73%"}
        ]

    }
]
INVESTOR_OBJ =[{'name': '李_2', 'time': '2023-06-18 20:16:00', 'percent': 2.141917321991371, 'initValue': 1400, 'assetsWhileJoin': 63962, 'protectValue': 0},
{'name': 'keqin', 'time': '2023-06-14 09:22:00', 'percent': 4.876972689780482, 'initValue': 3000, 'assetsWhileJoin': 57196, 'protectValue': 0}, 
{'name': '银杏家具_2', 'time': '2023-06-14 06:43:00', 'percent': 1.956913411541712, 'initValue': 1200, 'assetsWhileJoin': 55817, 'protectValue': 0}, 
{'name': 'cam', 'time': '2023-06-13 23:50:00', 'percent': 1.9496337715806333, 'initValue': 1189.66, 'assetsWhileJoin': 54353, 'protectValue': 0}, 
{'name': 'Miller', 'time': '2023-06-13 22:55:00', 'percent': 4.9300534733375905, 'initValue': 3000, 'assetsWhileJoin': 51203, 'protectValue': 0}, 
{'name': '汇金小哥哥', 'time': '2023-06-13 15:06:00', 'percent': 5.116619263728407, 'initValue': 3000, 'assetsWhileJoin': 46336, 'protectValue': 0}, 
{'name': 'VincentK', 'time': '2023-06-08 23:28:00', 'percent': 11.959704906573975, 'initValue': 6500, 'assetsWhileJoin': 36451, 'protectValue': 0}, 
{'name': '星星', 'time': '2023-06-08 17:32:00', 'percent': 5.56770806150077, 'initValue': 3005, 'assetsWhileJoin': 33193, 'protectValue': 0}, 
{'name': 'X_Gao', 'time': '2023-06-03 19:00:00', 'percent': 5.537910785653709, 'initValue': 2800, 'assetsWhileJoin': 28295, 'protectValue': 0}, 
{'name': '银杏家具', 'time': '2023-05-30 13:55:00', 'percent': 6.141056030728629, 'initValue': 2800, 'assetsWhileJoin': 22716, 'protectValue': 0}, 
{'name': '吴钊庆', 'time': '2023-05-28 20:11:00', 'percent': 6.11922299456006, 'initValue': 2601.49, 'assetsWhileJoin': 21180.85, 'protectValue': 198.5}, 
{'name': '一零二四', 'time': '2023-05-28 20:11:00', 'percent': 10.934480777159159, 'initValue': 4648.62, 'assetsWhileJoin': 21180.85, 'protectValue': 351.36}, 
{'name': '李', 'time': '2023-05-28 20:11:00', 'percent': 5.814754315297079, 'initValue': 2472.05, 'assetsWhileJoin': 21180.85, 'protectValue': 127.94},
 {'name': 'michael', 'time': '2023-05-28 20:11:00', 'percent': 23.52199314454432, 'initValue': 10000, 'assetsWhileJoin': 21180.85, 'protectValue': 0}, 
 {'name': 'ming', 'time': '2023-05-28 20:11:00', 'percent': 3.2540795756025496, 'initValue': 1383.42, 'assetsWhileJoin': 21180.85, 'protectValue': 0}]



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
            print(INFO_OBJ["p"]["all"][3])

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



SECOND_OPEN_OBJ_ARR = []

SECOND_OPEN_OBJ_ARR_UPDATE_TS = 0

SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME = random.randint(1,60)

TODAY_PROFIT = 0

LAST_GENERATE_TS = 0

def generateObj():
    global LAST_GENERATE_TS,TODAY_PROFIT,MAKER_COMMISSION_RATE,TAKER_COMMISSION_RATE,INFO_OBJ,FUNCTION_CLIENT,LAST_GENERATE_TIME,INVESTOR_OBJ,HISTORY_INVESTOR_OBJ,SECOND_OPEN_OBJ_ARR,SECOND_OPEN_OBJ_ARR_UPDATE_TS,SECOND_OPEN_OBJ_ARR_UPDATE_DELAY_TIME
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



        allPositionArr = []
        accountBalanceValue = 0

        thisIP = "172.24.207.4"

        thisKey = "LLLhzRFM6hFoaYdOZl3pSTsxKGuMKdIFto66mf9y83j8xPx7wvGe4f6lycqIsFNC"

        result = {}
        normal = False
        errorTime = 0
        while not normal:
            try:
                url = "http://"+thisIP+"/"+thisKey[0:10]+".json"
                result = requests.request("GET", url,timeout=(0.25,0.25)).json()
                normal = True
            except Exception as e:
                errorTime = errorTime+1
                time.sleep(1)
                if errorTime>3:
                    ex = traceback.format_exc()
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
                    errorTime= 0

        accountBalanceValue = result["balance"]

        allPositionValue = 0
        positionArr = []
        for a in range(len(result["positionArr"])):
            positionValue = int(abs(float(result["positionArr"][a]["entryPrice"])*float(result["positionArr"][a]["positionAmt"])))
            allPositionValue = allPositionValue + positionValue
            direction = "shorts"
            if float(result["positionArr"][a]["positionAmt"])>0:
                direction = "longs"
            positionArr.append({
                    "value":positionValue,
                    "symbol":result["positionArr"][a]["symbol"],
                    "direction":direction,
                    "entryPrice":float(result["positionArr"][a]["entryPrice"])
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


        sql = "SELECT income FROM `income_history_take` where `incomeType` ='TRANSFER' and id>3251"

        transferData = FUNCTION_CLIENT.mysql_select(sql,[])
        allTransferValue = 0
        for i in range(len(transferData)):
            allTransferValue = allTransferValue+transferData[i][0]

        fromLastInvestor = []
        lastOneDays = []
        lastSevenDays = []
        lastOneMonth = []
        TODAY_PROFIT = todayProfit

        yesterdayInfo = {}
        leftProfit = 0
        withdrawProfit = INFO_OBJ["p"]["all"][0]*0.6-INFO_OBJ["c"]["all"][0]*0.3*0.6+leftProfit
        if withdrawProfit>0:
            yesterdayInfo={
                            "withdraw":withdrawProfit,
                            "allTransferValue":abs(allTransferValue),
                            "toMeProfit":(withdrawProfit*0.6)
                        }
        else:
            yesterdayInfo={
                            "withdraw":0,
                            "allTransferValue":abs(allTransferValue),
                            "toMeProfit":0
                        }
        pushObj = {
            "yesterdayInfo":yesterdayInfo,
            "allTransferValue":abs(allTransferValue),
            "positionArr":positionArr,
            "todayProfit":todayProfit,
            "oneDayVol":int(abs(oneDayVol)),
            "oneDayProfit":int(oneDayProfit),
            "allPositionValue":int(allPositionValue),
            "secondOpenObjArr":INFO_OBJ,
            "accountBalanceValue":accountBalanceValue,
            "bigLossTradeArr":bigLossTradeArr,
            "investPercentObjArr":INVESTOR_OBJ,
            "systemStatus":systemStatus,
            "systemUpdateTs":systemUpdateTs,
            "runTime":allRunTime,
        }
        print(pushObj)
        LAST_GENERATE_TIME = nowTime
        FUNCTION_CLIENT.oss_put_obj(pushObj,"jl/"+nowTime+".json")

        FUNCTION_CLIENT.oss_put_obj(pushObj,"jl/a.json")

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
        sql = "select `positionValue`,`balance`,`ts`,`time` from position_record_take where balance>10000 order by id asc"
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
        FUNCTION_CLIENT.oss_put_obj(fromLastInvestorArr,"jl_change/fromLastInvestorArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastOneDayArr,"jl_change/lastOneDayArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastSevenDaysArr,"jl_change/lastSevenDaysArr.json")
        FUNCTION_CLIENT.oss_put_obj(lastOneMonthArr,"jl_change/lastOneMonthArr.json")
        FUNCTION_CLIENT.oss_put_obj(allArr,"jl_change/allArr.json")

UPDATE_DAY_INCOME_TS = 0

def updateDayIncome():
    global UPDATE_DAY_INCOME_TS,TODAY_PROFIT
    print("update_day_income")
    now = int(time.time())
    if now - UPDATE_DAY_INCOME_TS>60*15:
        UPDATE_DAY_INCOME_TS = now
        incomeDayTableName = "income_history_take_day"
        incomeTableName = "income_history_take"
        sql = "select `dayBeginTime` from "+incomeDayTableName+" order by id desc limit 1"
        lastBinanceTsData = FUNCTION_CLIENT.mysql_select(sql,[])


        initIncomeDayTime = "2023-07-09 00:00:00"
        initIncomeDayTs = FUNCTION_CLIENT.turn_ts_to_time(initIncomeDayTime)
        lastIncomeDayTs = 0
        if len(lastBinanceTsData)>0:
            lastIncomeDayTs = FUNCTION_CLIENT.turn_ts_to_time(lastBinanceTsData[0][0]) 
        if lastIncomeDayTs==0:
            lastIncomeDayTs= initIncomeDayTs
        nowTs = int(time.time())
        todayTs = FUNCTION_CLIENT.turn_ts_to_time(FUNCTION_CLIENT.turn_ts_to_day_time(int(time.time())))

        needInsertDay = int((todayTs - lastIncomeDayTs) /86400)
        print("todayTs:"+str(todayTs))
        print("lastIncomeDayTs:"+str(lastIncomeDayTs))
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
        FUNCTION_CLIENT.oss_put_obj(ossObj,"jl_day_income/data.json")

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
