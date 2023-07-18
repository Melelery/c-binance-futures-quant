#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果
import _thread
import decimal
import time
import requests
import json
import traceback
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
from commonFunction import FunctionClient


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="commission",connectMysql =True)

tableName = "income"
tableExit = False
sql ="show tables;"
tableData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tableData)):
    if tableData[a][0]==tableName:
        tableExit = True

print(tableExit)
if not tableExit:
    sql="""CREATE TABLE """+tableName+""" (
  `id` int NOT NULL AUTO_INCREMENT,
  `incomeType` varchar(255) DEFAULT NULL,
  `income` double(30,10) DEFAULT NULL,
  `bnbPrice` double(30,10) DEFAULT NULL,
  `asset` varchar(255) DEFAULT NULL,
  `trade_id` varchar(255) DEFAULT NULL,
  `binance_ts` bigint DEFAULT NULL,
  `symbol` varchar(255) DEFAULT NULL,
  `apiKey` varchar(255) DEFAULT NULL,
  `commission` double(30,10) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `my_ts` bigint DEFAULT NULL,
  `instrument_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=754 DEFAULT CHARSET=utf8mb3
;"""
    FUNCTION_CLIENT.mysql_commit(sql,[])


tableName = "income_history_take"
tableExit = False
sql ="show tables;"
tableData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tableData)):
    if tableData[a][0]==tableName:
        tableExit = True

print(tableExit)
if not tableExit:
    sql="""CREATE TABLE `"""+tableName+"""` (
  `id` int NOT NULL AUTO_INCREMENT,
  `incomeType` varchar(255) DEFAULT NULL,
  `income` double(30,10) DEFAULT NULL,
  `bnbPrice` double(30,10) DEFAULT NULL,
  `asset` varchar(255) DEFAULT NULL,
  `trade_id` varchar(255) DEFAULT NULL,
  `binance_ts` bigint DEFAULT NULL,
  `symbol` varchar(255) DEFAULT NULL,
  `apiKey` varchar(255) DEFAULT NULL,
  `commission` double(30,10) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `my_ts` bigint DEFAULT NULL,
  `instrument_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
;
"""
    FUNCTION_CLIENT.mysql_commit(sql,[])


privateIP = FUNCTION_CLIENT.get_private_ip()


BINANCE_API_KEY =""

BINANCE_API_SECRET =""

LAST_SHORT_LOSS_LOCK_TS = 0

SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("commission_",""))

INCOME_TABLE_NAME_ARR = ["income_history_take"]

TEMP_INCOME_TABLE_NAME_ARR = ["income"]


BINANCE_API_KEY_ARR =[""]
BINANCE_API_SECRET_ARR =[""]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])

INCOME_TABLE_NAME = INCOME_TABLE_NAME_ARR[MACHINE_INDEX]

TEMP_INCOME_TABLE_NAME = TEMP_INCOME_TABLE_NAME_ARR[MACHINE_INDEX]


def getBNBPrice():
    nowPrice = 0
    tryTime = 0
    while nowPrice==0:
        try:
            url = "https://api.binance.com/api/v1/depth?symbol=BNBUSDT&limit=5"
            response = requests.request("GET", url,timeout=(3,7)).json()
            nowPrice = (float(response['asks'][0][0])+float(response['bids'][0][0])) /2
        except Exception as e:
            tryTime = tryTime+1
            time.sleep(1)
            if tryTime>3:
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("读取bnb价格出错")
            print(e)
    return nowPrice

INCOME_TABLE_DELETE_TS = 0
UPDATE_TS = 0
def record_commission():
    global MACHINE_INDEX,TEMP_INCOME_TABLE_NAME,INCOME_TABLE_NAME,REQUEST_CLIENT,BINANCE_API_KEY_ARR,BINANCE_API_SECRET_ARR,INCOME_TABLE_NAME_ARR,FUNCTION_CLIENT,INCOME_TABLE_DELETE_TS,UPDATE_TS

    now = int(time.time()*1000)
    if now - UPDATE_TS>1000:
        UPDATE_TS = now
        if now - INCOME_TABLE_DELETE_TS>3600000:
            INCOME_TABLE_DELETE_TS = now
            sql = "delete from "+TEMP_INCOME_TABLE_NAME+" where binance_ts<%s" 
            FUNCTION_CLIENT.mysql_commit(sql,[now-86400000])


        sql = "select `binance_ts`,`income`,`trade_id`,`symbol` from "+TEMP_INCOME_TABLE_NAME+"  order by id desc"
        incomeData = FUNCTION_CLIENT.mysql_select(sql,[])
        lasIncomeTs = 0
        if len(incomeData)>0:
            lasIncomeTs = incomeData[0][0]

        fourHoursProfitObj = {}
        oneDayProfitObj = {}
        allOneDayProfit = 0
        allFourHoursProfit= 0
        for i in range(len(incomeData)):
            symbol = incomeData[i][3]
            profit = incomeData[i][1]

            binanceTs = incomeData[i][0]
            allOneDayProfit = allOneDayProfit+profit
            if now - binanceTs<4*60*60*1000:
                allFourHoursProfit = allFourHoursProfit+profit
                if symbol in fourHoursProfitObj:
                    fourHoursProfitObj[symbol] =  fourHoursProfitObj[symbol]+profit
                else:
                    fourHoursProfitObj[symbol] = profit
            if symbol in oneDayProfitObj:
                oneDayProfitObj[symbol] =  oneDayProfitObj[symbol]+profit
            else:
                oneDayProfitObj[symbol] = profit

            if not(symbol in fourHoursProfitObj):
                fourHoursProfitObj[symbol] = 0
        banSymbolArr = []

        for key in fourHoursProfitObj:
            if fourHoursProfitObj[key]<=-150 or oneDayProfitObj[key]<=-1800:
                banSymbolArr.append(key)

        if allOneDayProfit<=-3000:
            banSymbolArr = ["ALL"]


        sendStr = ""
        for a in range(len(banSymbolArr)):

            if sendStr=="":
                sendStr = banSymbolArr[a]
            else:
                sendStr = sendStr+"@"+ banSymbolArr[a]
        if sendStr=="":
            sendStr = "AAAUSDT"
        sendStr = "abcoihsoaitowljd"+sendStr

        FUNCTION_CLIENT.send_to_ws_a(sendStr)


        sql = "select `binance_ts`,`incomeType`,`income`,`asset`,`trade_id` from "+INCOME_TABLE_NAME+"  order by id desc limit 2000"
        lastBinanceTsData = FUNCTION_CLIENT.mysql_select(sql,[])
        lastBinanceTs = 0
        if len(lastBinanceTsData)>0:
            lastBinanceTs = lastBinanceTsData[0][0]

        result = REQUEST_CLIENT.get_income_history_with_no_symbol()
        result = json.loads(result)

        if "code" in result:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(result))
        else:
            for i in range(len(result)):
                trade_id = str(result[i]['tradeId'])
                binance_ts = str(result[i]['time'])
                incomeType = str(result[i]['incomeType'])
                income = str(result[i]['income'])
                asset = str(result[i]['asset'])
                info = str(result[i]['info'])
                my_ts = str(int(time.time()))
                symbol = str(result[i]['symbol'])
                if incomeType=="REALIZED_PNL":
                    isExit = False
                    scanCount = len(incomeData)
                    if scanCount>2000:
                        scanCount = 2000
                    for b in range(scanCount):
                        if (str(int(incomeData[b][0]))==str(int(binance_ts))) and (format(float(incomeData[b][1]),'.8f') == format(float(income),'.8f')) and  (str(incomeData[b][2]) == str(trade_id)):
                            isExit = True     
                    if not isExit:
                        insertSQLStr = "('"+str(income)+"','"+trade_id+"','"+binance_ts+"','"+symbol+"')"
                        sql = "INSERT INTO "+TEMP_INCOME_TABLE_NAME+" ( `income`,`trade_id`,`binance_ts`,`symbol`)  VALUES "+insertSQLStr+";" 
                        FUNCTION_CLIENT.mysql_commit(sql,[])

            bnbPrice = getBNBPrice()

            for i in range(len(result)):
                trade_id = str(result[i]['tradeId'])
                binance_ts = str(result[i]['time'])
                incomeType = str(result[i]['incomeType'])
                income = str(result[i]['income'])
                asset = str(result[i]['asset'])
                info = str(result[i]['info'])
                my_ts = str(int(time.time()))
                symbol = str(result[i]['symbol'])

                isExit = False

                for b in range(len(lastBinanceTsData)):
                    if (str(int(lastBinanceTsData[b][0]))==str(int(binance_ts))) and (str(lastBinanceTsData[b][1]) == str(incomeType)) and (format(float(lastBinanceTsData[b][2]),'.8f') == format(float(income),'.8f')) and (str(lastBinanceTsData[b][3]) == str(asset)) and (str(lastBinanceTsData[b][4]) == str(trade_id)):
                        isExit = True     
                if not isExit and result[i]['time']>1688256000000:
                    insertSQLStr = "('"+str(incomeType)+"','"+str(income)+"','"+str(asset)+"','"+info+"','"+trade_id+"','"+binance_ts+"','"+my_ts+"','"+symbol+"','"+symbol+"','"+symbol+"','"+str(bnbPrice)+"')"
                    sql = "INSERT INTO "+INCOME_TABLE_NAME+" ( `incomeType`,`income`,`asset`,`info`,`trade_id`,`binance_ts`,`my_ts`,`symbol`,`instrument_id`,`coin`,`bnbPrice`)  VALUES "+insertSQLStr+";" 
                    FUNCTION_CLIENT.mysql_commit(sql,[])


while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        record_commission()
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(1)
        print(e)
    time.sleep(1)
