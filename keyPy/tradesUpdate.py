#!/usr/bin/python3.10
# coding=utf-8
import traceback
import json
import random
import time
import requests
import socket
import decimal
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
from commonFunction import FunctionClient

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]

SYMBOL_OBJ_ARR = []

for i in range(len(TRADE_SYMBOL_ARR)):
    SYMBOL_OBJ_ARR.append({
            "coin":TRADE_SYMBOL_ARR[i]["coin"],
            "binanceSymbol":TRADE_SYMBOL_ARR[i]["symbol"],
            "bybitSymbol":"",
            "okexSymbol":""
        })

def updateOkexSymbolInfo():
    global SYMBOL_OBJ_ARR
    url = "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
    response = requests.request("GET", url,timeout=(3,7)).json()
    resultArr = response["data"]
    for a in range(len(resultArr)):
        for b in range(len(SYMBOL_OBJ_ARR)):
            if resultArr[a]["instType"]=="SWAP" and resultArr[a]["ctValCcy"].upper()==SYMBOL_OBJ_ARR[b]["coin"].upper():
                SYMBOL_OBJ_ARR[b]["okexSymbol"] = resultArr[a]["instId"]

def updateBybitSymbolInfo():
    global SYMBOL_OBJ_ARR
    url = "https://api.bybit.com/v5/market/instruments-info?category=linear&limit=1000"
    response = requests.request("GET", url,timeout=(3,7)).json()
    resultArr = response["result"]["list"]
    for a in range(len(resultArr)):
        for b in range(len(SYMBOL_OBJ_ARR)):
            if resultArr[a]["symbol"]==SYMBOL_OBJ_ARR[b]["binanceSymbol"]:
                SYMBOL_OBJ_ARR[b]["bybitSymbol"] = resultArr[a]["symbol"]

updateOkexSymbolInfo()
updateBybitSymbolInfo()



def takeElemZero(elem):
    return int(elem[0])

def getOkexKline(startTs,symbol):
    url = "https://www.okx.com/api/v5/market/history-candles?instId="+symbol+"&limit=100&bar=15m&after="+str(int(startTs))
    okexResponseA = requests.request("GET", url,timeout=(3,7)).json()
    okexDataA = okexResponseA["data"]
    okexDataA.sort(key=takeElemZero,reverse=False)

    url = "https://www.okx.com/api/v5/market/history-candles?instId="+symbol+"&limit=100&bar=15m&after="+str(int(startTs)-15*60*100*1000)
    okexResponseB = requests.request("GET", url,timeout=(3,7)).json()
    okexDataB = okexResponseB["data"]
    okexDataB.sort(key=takeElemZero,reverse=True)

    url = "https://www.okx.com/api/v5/market/history-candles?instId="+symbol+"&limit=100&bar=15m&after="+str(int(startTs)-15*60*200*1000)
    okexResponseC = requests.request("GET", url,timeout=(3,7)).json()
    okexDataC = okexResponseC["data"]
    okexDataC.sort(key=takeElemZero,reverse=True)

    url = "https://www.okx.com/api/v5/market/history-candles?instId="+symbol+"&limit=100&bar=15m&after="+str(int(startTs)-15*60*300*1000)
    okexResponseD = requests.request("GET", url,timeout=(3,7)).json()
    okexDataD = okexResponseD["data"]
    okexDataD.sort(key=takeElemZero,reverse=True)

    url = "https://www.okx.com/api/v5/market/history-candles?instId="+symbol+"&limit=100&bar=15m&after="+str(int(startTs)-15*60*400*1000)
    okexResponseE = requests.request("GET", url,timeout=(3,7)).json()
    okexDataE = okexResponseE["data"]
    okexDataE.sort(key=takeElemZero,reverse=True)

    okexKlineArr = okexDataA


    for i in range(len(okexDataB)):
        okexDataB[i].append("B")
        okexKlineArr.insert(0,okexDataB[i])

    for i in range(len(okexDataC)):
        okexDataC[i].append("C")
        okexKlineArr.insert(0,okexDataC[i])

    for i in range(len(okexDataD)):
        okexDataD[i].append("D")
        okexKlineArr.insert(0,okexDataD[i])

    for i in range(len(okexDataE)):
        okexDataE[i].append("E")
        okexKlineArr.insert(0,okexDataE[i])

    for i in range(len(okexKlineArr)):
        if i+1<len(okexKlineArr):
            if int(okexKlineArr[i][0]) !=int(okexKlineArr[i+1][0])-15*60*1000:
                print("---------------------------------")
                print(i)
                print(int(okexKlineArr[i+1][0])-int(okexKlineArr[i][0]))
                print(okexKlineArr[i])
                print(okexKlineArr[i+1])
    return okexKlineArr

def getBybitKline(startTs,symbol):

    url = "https://api.bybit.com/v5/market/kline?category=linear&symbol="+symbol+"&limit=200&interval=15&end="+str(int(startTs))
    bybitResponseA = requests.request("GET", url,timeout=(3,7)).json()
    bybitDataA = bybitResponseA["result"]["list"]
    bybitDataA.sort(key=takeElemZero,reverse=False)

    url = "https://api.bybit.com/v5/market/kline?category=linear&symbol="+symbol+"&limit=200&interval=15&end="+str(int(startTs)-15*60*200*1000)
    bybitResponseB = requests.request("GET", url,timeout=(3,7)).json()
    bybitDataB = bybitResponseB["result"]["list"]
    bybitDataB.sort(key=takeElemZero,reverse=True)

    url = "https://api.bybit.com/v5/market/kline?category=linear&symbol="+symbol+"&limit=100&interval=15&end="+str(int(startTs)-15*60*400*1000)
    bybitResponseC = requests.request("GET", url,timeout=(3,7)).json()
    bybitDataC = bybitResponseC["result"]["list"]
    bybitDataC.sort(key=takeElemZero,reverse=True)


    bybitKlineArr = bybitDataA


    for i in range(len(bybitDataB)):
        bybitDataB[i].append("B")
        bybitKlineArr.insert(0,bybitDataB[i])

    for i in range(len(bybitDataC)):
        bybitDataC[i].append("C")
        bybitKlineArr.insert(0,bybitDataC[i])

    for i in range(len(bybitKlineArr)):
        if i+1<len(bybitKlineArr):
            if int(bybitKlineArr[i][0]) !=int(bybitKlineArr[i+1][0])-15*60*1000:
                print("---------------------------------")
                print(i)
                print(int(bybitKlineArr[i+1][0])-int(bybitKlineArr[i][0]))
                print(bybitKlineArr[i])
                print(bybitKlineArr[i+1])
    return bybitKlineArr

def getBinanceKline(startTs,symbol):
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+symbol+"&endTime="+str(int(startTs))+"&interval=15m&limit=500"
    responseB = requests.request("GET", url,timeout=(3,7)).json()
    responseB.sort(key=takeElemZero,reverse=False)
    return responseB

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

TRADE_SYMBOL_ARR =  []

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]

BINANCE_API_KEY ="b3ZkI4KqqJ6EKw0MeDgmcCbinrtIo5nka9MDCb0mwCVmmQaROozMtJiTv4HH4NAv"

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="recordOrders",connectMysql =True)

PRIVATE_IP = FUNCTION_CLIENT.get_private_ip()

POSITION_ARR = []

POSITION_SERVER_IP_INDEX = 0

POSITION_UPDATE_TS = 0

ACCOUNT_BALANCE_VALUE = 0

def getBinancePositionFromMyServer():
    global FUNCTION_CLIENT,POSITION_ARR,BINANCE_API_KEY,POSITION_SERVER_IP_INDEX,POSITION_UPDATE_TS,ACCOUNT_BALANCE_VALUE
    errorTime = 0
    while errorTime<2:
        result = {}
        try:

            if POSITION_SERVER_IP_INDEX==0:
                thisIP = "172.24.207.96"
                POSITION_SERVER_IP_INDEX = 1
            elif POSITION_SERVER_IP_INDEX==1:
                thisIP = "172.24.207.4"
                POSITION_SERVER_IP_INDEX = 0


            url = "http://"+thisIP+"/"+BINANCE_API_KEY[0:10]+".json"
            result = requests.request("GET", url,timeout=(0.5,0.5)).json()
            positionUpdate= False

            if result["balance"]>0:
                ACCOUNT_BALANCE_VALUE = result["balance"]

            for i in range(len(result["positionArr"])):
                if result["positionArr"][i]["updateTime"]>=POSITION_UPDATE_TS:
                    positionUpdate = True
                    POSITION_UPDATE_TS = result["positionArr"][i]["updateTime"]
            if len(result["positionArr"])>0 and positionUpdate:
                POSITION_ARR = []
                for i in range(len(result["positionArr"])):
                    if float(result["positionArr"][i]["entryPrice"])!=0:
                        POSITION_ARR.append(result["positionArr"][i])
            errorTime = 100
        except Exception as e:
            errorTime = errorTime +1
            if errorTime>=2:
                FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            time.sleep(0.25)
    if errorTime==100:
        return True
    else:
        return False

def getPositionInfoArrBySymbol(symbol):
    global POSITION_ARR
    for positionIndex in range(len(POSITION_ARR)):
        thisSymbol = POSITION_ARR[positionIndex]["symbol"]
        symbolPositionAmt = float(POSITION_ARR[positionIndex]["positionAmt"])
        symbolCost = float(POSITION_ARR[positionIndex]["entryPrice"])
        if thisSymbol == symbol:
            return [symbolPositionAmt,symbolCost,True]
    return [0,0,False]


RECORD_OBJ = {}

def update():
    global TRADE_SYMBOL_ARR,RECORD_OBJ,PRIVATE_IP,ACCOUNT_BALANCE_VALUE
    now = int(time.time()*1000)
    sql = "select `id`,`symbol`,`beginTs` from trades_take where status='tradeBegin'"
    tradesData = FUNCTION_CLIENT.mysql_select(sql,[])

    for tradesDataIndex in range(len(tradesData)):
        tradeBeginTs  = tradesData[tradesDataIndex][2]
        dataID = tradesData[tradesDataIndex][0]
        symbol = tradesData[tradesDataIndex][1]
        symbolPositionInfoArr = getPositionInfoArrBySymbol(symbol)
        positionCost = symbolPositionInfoArr[1]
        symbolPositionAmt = symbolPositionInfoArr[0]
        positionValue = abs(int(positionCost*symbolPositionAmt))


        if ((not (symbol in RECORD_OBJ)) or RECORD_OBJ[symbol]["status"]=="tradeEnd"):
            RECORD_OBJ[symbol] = {"balance":ACCOUNT_BALANCE_VALUE,"status":"tradeBegin","beginTs":now,"symbol":symbol,"value":positionValue,"amount":symbolPositionAmt,"cost":positionCost}
            print(RECORD_OBJ)
        if ( symbol in RECORD_OBJ) and RECORD_OBJ[symbol]["status"]=="tradeBegin" and positionValue>RECORD_OBJ[symbol]["value"]:
            RECORD_OBJ[symbol]["value"] = positionValue
            RECORD_OBJ[symbol]["amount"] = symbolPositionAmt
            RECORD_OBJ[symbol]["cost"] = positionCost
        if ( symbol in RECORD_OBJ) and RECORD_OBJ[symbol]["status"]=="tradeBegin" and positionValue==0 and now-tradeBeginTs>60000:
            RECORD_OBJ[symbol]["status"]="tradeEnd"
            insertBalance = RECORD_OBJ[symbol]["balance"]
            if insertBalance==0:
                insertBalance = ACCOUNT_BALANCE_VALUE
            sql = "update trades_take set `value` = %s,`amount`=%s,`cost`=%s,`balance`=%s,endTs=%s,`status`='tradeEnd' where id=%s"
            FUNCTION_CLIENT.mysql_commit(sql,[RECORD_OBJ[symbol]["value"],RECORD_OBJ[symbol]["amount"],RECORD_OBJ[symbol]["cost"],insertBalance,now,dataID])

def takeElemZero(elem):
    return float(elem[0])

UPDATE_PROFIT_TS = 0
def updateProfit():
    global UPDATE_PROFIT_TS,SYMBOL_OBJ_ARR
    now = int(time.time()*1000)
    if now - UPDATE_PROFIT_TS>1*60*1000:
        sql = "select binance_ts from income_history_take order by id desc limit 1"
        incomeHistoryData = FUNCTION_CLIENT.mysql_select(sql,[])
        lastBinanceUpdateTs = incomeHistoryData[0][0]

        UPDATE_PROFIT_TS = now
        sql = "select  `beginTs`,`endTs`,symbol,id,balance,direction,symbol from trades_take where status='tradeEnd' and endTs<%s"
        tradesRecordData = FUNCTION_CLIENT.mysql_select(sql,[lastBinanceUpdateTs-5*60*1000])
        for i in range(len(tradesRecordData)):
            tradeBeginTs =  tradesRecordData[i][0]
            tradeEndTs =  tradesRecordData[i][1]
            tradeRecordDataID = tradesRecordData[i][3]
            balance = tradesRecordData[i][4]
            direction = tradesRecordData[i][5]
            binanceSymbol = tradesRecordData[i][6]
            sql = "select income,binance_ts,incomeType,bnbPrice,asset,symbol from income_history_take  where binance_ts>=%s and binance_ts<=%s and symbol=%s"
            data = FUNCTION_CLIENT.mysql_select(sql,[tradeBeginTs,tradeEndTs,tradesRecordData[i][2]])
            profit = 0
            commission = 0

            bybitSymbol = ""
            okexSymbol = ""
            for i in range(len(SYMBOL_OBJ_ARR)):
                if SYMBOL_OBJ_ARR[i]["binanceSymbol"]==binanceSymbol:
                    bybitSymbol = SYMBOL_OBJ_ARR[i]["bybitSymbol"]
                    okexSymbol = SYMBOL_OBJ_ARR[i]["okexSymbol"]
                    break

            for i in range(len(data)):
                income = data[i][0]
                binanceTs = data[i][1]
                incomeType = data[i][2]
                bnbPrice = data[i][3]
                asset = data[i][4]
                symbol = data[i][5]
                realIncome = 0
                if asset=="BNB":
                    realIncome = income*bnbPrice
                else:
                    realIncome = income
                if incomeType=="COMMISSION":
                    commission = commission+realIncome
                if incomeType=="REALIZED_PNL" or incomeType=="COMMISSION":
                    profit = profit+realIncome

            print("commission:"+str(commission))
            print("profit:"+str(profit))
            print("bybitSymbol:"+str(bybitSymbol))
            print("okexSymbol:"+str(okexSymbol))
            if commission!=0 or profit!=0:
                profitPercentByBalance = FUNCTION_CLIENT.get_percent_num(profit,balance)
                priceRate = 0
                try:
                    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+binanceSymbol+"&startTime="+str(tradeBeginTs-60000)+"&endTime="+str(tradeEndTs+60000)+"&interval=1m"
                    response = requests.request("GET", url,timeout=(3,7)).json()

                    # url = "https://fapi.binance.com/fapi/v1/klines?symbol="+symbol+"&endTime="+str(tradeBeginTs-15*60000)+"&interval=15m&limit=999"
                    # responseB = requests.request("GET", url,timeout=(3,7)).json()
                    bybitHoursVolArr = []
                    if bybitSymbol!="":
                        bybitKlineArr = getBybitKline(tradeBeginTs-15*60000,bybitSymbol)
                        bybitHoursVolArr = []
                        for i in range(125):
                            bybitHoursVolArr.append(0)
                        for i in range(len(bybitKlineArr)):
                            index  = int(i/4)
                            bybitHoursVolArr[index] = bybitHoursVolArr[index]+float(bybitKlineArr[len(bybitKlineArr)-1-i][6])
                        for i in range(len(bybitHoursVolArr)):
                            bybitHoursVolArr[i] = int(bybitHoursVolArr[i])

                    okexHoursVolArr = []
                    if okexSymbol!="":
                        okexKlineArr = getOkexKline(tradeBeginTs-15*60000,okexSymbol)
                        okexHoursVolArr = []
                        for i in range(125):
                            okexHoursVolArr.append(0)
                        for i in range(len(okexKlineArr)):
                            index  = int(i/4)
                            okexHoursVolArr[index] = okexHoursVolArr[index]+float(okexKlineArr[len(okexKlineArr)-1-i][7])
                        for i in range(len(okexHoursVolArr)):
                            okexHoursVolArr[i] = int(okexHoursVolArr[i])

                    binanceKlineArr = getBinanceKline(tradeBeginTs-15*60000,binanceSymbol)
                    binanceHoursVolArr = []
                    for i in range(125):
                        binanceHoursVolArr.append(0)
                    for i in range(len(binanceKlineArr)):
                        index  = int(i/4)
                        binanceHoursVolArr[index] = binanceHoursVolArr[index]+float(binanceKlineArr[len(binanceKlineArr)-1-i][7])
                    for i in range(len(binanceHoursVolArr)):
                        binanceHoursVolArr[i] = int(binanceHoursVolArr[i])


                    highPrice = 0
                    lowPrice = 9999999
                    for i in range(len(response)):
                        if float(response[i][2])>highPrice:
                            highPrice = float(response[i][2])
                        if float(response[i][3])<lowPrice:
                            lowPrice = float(response[i][3])
                    if direction=="s":
                        priceRate = FUNCTION_CLIENT.get_percent_num(highPrice-lowPrice,lowPrice)
                    elif direction=="l":
                        priceRate = FUNCTION_CLIENT.get_percent_num(highPrice-lowPrice,lowPrice)

                    profitPercentByBalance = FUNCTION_CLIENT.get_percent_num(profit,balance)
                    sql = "update trades_take set profit=%s,commission=%s,status=%s,profitPercentByBalance=%s,volInfo=%s,extraInfo=%s where id=%s"
                    FUNCTION_CLIENT.mysql_commit(sql,[profit,commission,"updateProfit",profitPercentByBalance,json.dumps({"binanceHoursVolArr":binanceHoursVolArr,"okexHoursVolArr":okexHoursVolArr,"bybitHoursVolArr":bybitHoursVolArr}),json.dumps({"priceRate":priceRate}),tradeRecordDataID])
                except Exception as e:
                    time.sleep(3)
                    ex = traceback.format_exc()
                    print(ex)
            else:
                sql = "update trades_take set status=%s where id=%s"
                FUNCTION_CLIENT.mysql_commit(sql,["updateProfitFail",tradeRecordDataID])


while 1:
    getBinancePositionFromMyServer()
    update()
    updateProfit()
    time.sleep(1)