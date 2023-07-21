#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果
import decimal
import time
import requests
import json
import traceback
from datetime import datetime
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="positionReord")

POSITION_TABLE_NAME = "position_record"

tableExit = False
sql ="show tables;"
tableData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tableData)):
    if tableData[a][0]==POSITION_TABLE_NAME:
        tableExit = True

print(tableExit)
if not tableExit:
    sql="""CREATE TABLE `"""+POSITION_TABLE_NAME+"""` (
`id` int NOT NULL AUTO_INCREMENT,
`symbol` varchar(255) DEFAULT NULL,
`unrealizedProfit` double(30,10) DEFAULT NULL,
`positionAmt` double(30,10) DEFAULT NULL,
`ts` bigint DEFAULT NULL,
`time` varchar(255) DEFAULT NULL,

`positionValue` double(30,10) DEFAULT NULL,
`balance` double(30,10) DEFAULT NULL,
`updateProfitAndCommission` int DEFAULT 0,
`profit` double(30,10) DEFAULT NULL,
`commission` double(30,10) DEFAULT NULL,
`makerCommission` double(30,10) DEFAULT NULL,
PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
;
"""
    FUNCTION_CLIENT.mysql_commit(sql,[])

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

TRADE_SYMBOL_ARR =  []

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]


print(TRADE_SYMBOL_ARR)


PRICE_DECIMAL_OBJ = {}

AMOUNT_DECIMAL_OBJ = {}

PRICE_TICK_OBJ = {}

PRICE_DECIMAL_AMOUNT_OBJ = {}

AMOUNT_DECIMAL_AMOUNT_OBJ = {}

MARKET_MAX_SIZE_OBJ = {}


def updateSymbolInfo():
    global PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,PRICE_DECIMAL_AMOUNT_OBJ,AMOUNT_DECIMAL_AMOUNT_OBJ,PRICE_TICK_OBJ,MARKET_MAX_SIZE_OBJ
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.request("GET", url,timeout=(3,7)).json()
    symbols = response['symbols']
    for i in range(len(symbols)):
        thisInstrumentID = symbols[i]['symbol']
        priceTick = 0
        priceDecimal = ""
        amountDecimal = ""
        priceDecimalAmount = ""
        amountDecimalAmount = ""
        for c in range(len(symbols[i]['filters'])):
            if symbols[i]['filters'][c]['filterType']=="PRICE_FILTER":
                priceTick=float(symbols[i]['filters'][c]['tickSize'])
                thisDecimal = 0
                initPara = 10
                for d in range(20):
                    thisDecimal = thisDecimal+1
                    initPara = round(initPara/10,10)
                    if initPara==float(symbols[i]['filters'][c]['tickSize']):
                        break
                priceDecimal = "%."+str(thisDecimal-1)+"f"
                priceDecimalAmount= str(thisDecimal-1)
            if symbols[i]['filters'][c]['filterType']=="LOT_SIZE":
                thisDecimal = 0
                initPara = 10
                for d in range(20):
                    thisDecimal = thisDecimal+1
                    initPara = round(initPara/10,10)
                    if initPara==float(symbols[i]['filters'][c]['stepSize']):
                        break
                amountDecimal = "%."+str(thisDecimal-1)+"f"
                amountDecimalAmount = str(thisDecimal-1)
            if symbols[i]['filters'][c]['filterType']=="MARKET_LOT_SIZE":
                MARKET_MAX_SIZE_OBJ[thisInstrumentID] = float(symbols[i]['filters'][c]['maxQty'])
        PRICE_DECIMAL_OBJ[thisInstrumentID] = priceDecimal
        AMOUNT_DECIMAL_OBJ[thisInstrumentID] = amountDecimal
        PRICE_TICK_OBJ[thisInstrumentID] = priceTick
        PRICE_DECIMAL_AMOUNT_OBJ[thisInstrumentID] = priceDecimalAmount
        AMOUNT_DECIMAL_AMOUNT_OBJ[thisInstrumentID] = amountDecimalAmount

updateSymbolInfo()

while not "BTCUSDT" in PRICE_DECIMAL_OBJ:
    updateSymbolInfo()
    time.sleep(1)

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


def getFutureDepthBySymbol(symbol,limit):
    response = {}
    errorTime = 0
    while errorTime<100:
        try:
            url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
            response = requests.request("GET", url,timeout=(0.5,0.5)).json()
            errorTime = 100
        except Exception as e:
            print(e)
            errorTime = errorTime+1
            time.sleep(errorTime*0.5)
    return response


UPDATE_TS = 0
def record_position():
    global POSITION_TABLE_NAME,BINANCE_API_KEY_ARR,BINANCE_API_SECRET_ARR,TABLE_NAME_ARR,UPDATE_TS,ACCOUNT_BALANCE_VALUE,EIGHT_HOURS_PROFIT,SYMBOL_ARR,PRICE_DECIMAL_OBJ

    now = int(time.time())
    allPositionAmt = 0
    allUnrealizedProfit = 0
    allPositionValue = 0

    if now - UPDATE_TS>60:
        UPDATE_TS = now

        getBinancePositionFromMyServer()
        for tradeSymbolIndex in range(len(TRADE_SYMBOL_ARR)):
            symbol = TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbol"]
            symbolPositionInfoArr = getPositionInfoArrBySymbol(symbol)
            symbolPositionAmt = symbolPositionInfoArr[0]
            symbolCost = symbolPositionInfoArr[1]
            if symbolCost!=0:
                depthObj = getFutureDepthBySymbol(symbol,5)
                midPrice = (float(depthObj["bids"][0][0])+float(depthObj["asks"][0][0])) /2
                unrealizedProfit = symbolPositionAmt*(midPrice-symbolCost)
                symbolCost =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (symbolCost))

                allUnrealizedProfit = allUnrealizedProfit+unrealizedProfit
                allPositionAmt = allPositionAmt+symbolPositionInfoArr[0]

                allPositionValue = allPositionValue+abs(symbolPositionAmt*midPrice)

        insertSQLStr = "('all','"+str(allUnrealizedProfit)+"','"+str(allPositionAmt)+"','"+str(now)+"','"+str(FUNCTION_CLIENT.turn_ts_to_time(now))+"','"+str(allPositionValue)+"','"+str(ACCOUNT_BALANCE_VALUE)+"')"
        sql = "INSERT INTO "+POSITION_TABLE_NAME+" ( `symbol`,`unrealizedProfit`, `positionAmt`,`ts`,`time`,`positionValue`,`balance`)  VALUES "+insertSQLStr+";" 
        FUNCTION_CLIENT.mysql_commit(sql,[])

UPDATE_PROFIT_AND_COMMISSION_TS  = 0
def updateProfitAndCommission():
    global UPDATE_PROFIT_AND_COMMISSION_TS,ACCOUNT_SYMBOL,POSITION_TABLE_NAME
    now = int(time.time())
    if now - UPDATE_PROFIT_AND_COMMISSION_TS>60:
        UPDATE_PROFIT_AND_COMMISSION_TS = now

        sql = "select ts,id from "+POSITION_TABLE_NAME+"  where ts<%s and updateProfitAndCommission=0 order by id desc"
        positionRecordData = FUNCTION_CLIENT.mysql_select(sql,[now-60*30])
        if len(positionRecordData)>1:
            for i in range(len(positionRecordData)-1):
                thisID = positionRecordData[i][1]
                sql = "SELECT `ts`,`id` from "+POSITION_TABLE_NAME+"  where `id` = (SELECT max(`id`) FROM "+POSITION_TABLE_NAME+" where `id`<%s)"
                lastPositionRecordData = FUNCTION_CLIENT.mysql_select(sql,[thisID])
                if len(lastPositionRecordData)>0:
                    endTs = positionRecordData[i][0]
                    beginTs = lastPositionRecordData[0][0]
                    allProfit = 0
                    allCommission = 0
                    allMakerCommission = 0
                    sql = "select income,incomeType,asset,bnbPrice from income_history_take  where binance_ts>%s and binance_ts<=%s  order by id asc"
                    incomeData = FUNCTION_CLIENT.mysql_select(sql,[beginTs*1000,endTs*1000])
                    for b in range(len(incomeData)):
                        if incomeData[b][1]=="COMMISSION":
                            if incomeData[b][2]=="BNB":
                                allCommission = allCommission+incomeData[b][0]*incomeData[b][3]
                            else:
                                allCommission = allCommission+incomeData[b][0]
                            if incomeData[b][0]>0:
                                if incomeData[b][2]=="BNB":
                                    allMakerCommission = allMakerCommission+incomeData[b][0]*incomeData[b][3]
                                else:
                                    allMakerCommission = allMakerCommission+incomeData[b][0]
                        if incomeData[b][1]=="REALIZED_PNL":
                            allProfit = allProfit+incomeData[b][0]
                    sql = "update "+POSITION_TABLE_NAME+" set profit=%s,commission=%s,makerCommission=%s,updateProfitAndCommission=1 where id =%s"
                    FUNCTION_CLIENT.mysql_commit(sql,[allProfit,allCommission,allMakerCommission,thisID])

ERROR_TIME = 0
while 1:
    try:
        record_position()
        updateProfitAndCommission()
        ERROR_TIME = 0
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(1)
        print(ex)
    time.sleep(3)
