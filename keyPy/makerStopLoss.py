#!/usr/bin/python3.10
# coding=utf-8
import _thread
import traceback
import json
import random
import time
import requests
import decimal
import math
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="makerStopLoss")

privateIP = FUNCTION_CLIENT.get_private_ip()

SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("makerStopLoss_",""))


BINANCE_API_KEY_ARR =["",""]
BINANCE_API_SECRET_ARR =["",""]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])

STOP_LOSS_SYMBOL = "s"


ORDER_ID_INDEX  = random.randint(1,100000)



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
    FUNCTION_CLIENT.send_lark_msg_limit_one_min("mainConsole updateSymbolInfo")
    updateSymbolInfo()
    time.sleep(1)

def takeElemZero(elem):
    return float(elem[0])


def getFutureDepthBySymbol(symbol,limit):
    response = {}
    try:
        url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
        response = requests.request("GET", url,timeout=(0.5,0.5)).json()
    except Exception as e:
        try:
            url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
            response = requests.request("GET", url,timeout=(1,1)).json()
        except Exception as e:
            try:
                url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
                response = requests.request("GET", url,timeout=(2,2)).json()
            except Exception as e:
                print(e)
    return response


def cancelOrder(symbol,clientOrderId):
    global FUNCTION_CLIENT,REQUEST_CLIENT
    try:
        result = REQUEST_CLIENT.cancel_order(symbol=symbol,orderId=clientOrderId)
    except Exception as e:
        print(e)
        try:
            result = REQUEST_CLIENT.cancel_order(symbol=symbol,orderId=clientOrderId)
        except Exception as e:
            print(e)
            try:
                result = REQUEST_CLIENT.cancel_order(symbol=symbol,orderId=clientOrderId)
            except Exception as e:
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("【cancel order error】，"+symbol)
                return False
    return True

def getKline(symbol,interval,limit):
    global FUNCTION_CLIENT
    nowPrice = 0
    klineDataArr = []
    errorTime = 0
    while len(klineDataArr)==0:
        try:
            url = "https://fapi.binance.com/fapi/v1/klines?symbol="+symbol+"&interval="+interval+"&limit="+str(limit)
            klineDataArr = requests.request("GET", url,timeout=(0.5+errorTime*0.25,0.5+errorTime*0.25)).json()
            klineDataArr.sort(key=takeElemZero,reverse=False)
        except Exception as e:
            errorTime = errorTime+1
            if errorTime>10:
                errorTime = 0
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("getKline error:"+str(e))
            print(e)
    return klineDataArr



def forceCloseShorts(symbol):
    global REQUEST_CLIENT,ORDER_ID_INDEX,MARKET_MAX_SIZE_OBJ

    marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseShorts_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.BUY, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        print(result)
    except Exception as e:
        print(e)
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseShorts_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.BUY, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        print(result)
    except Exception as e:
        print(e)

def forceCloseLongs(symbol):
    global REQUEST_CLIENT,ORDER_ID_INDEX,MARKET_MAX_SIZE_OBJ

    marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseShorts_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.SELL, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        print(result)
    except Exception as e:
        print(e)
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseShorts_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.SELL, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        print(result)
    except Exception as e:
        print(e)


def cancelBinanceOrder(symbol):
    global FUNCTION_CLIENT,REQUEST_CLIENT
    result= {}
    try:
        result = REQUEST_CLIENT.cancel_all_orders(symbol=symbol)
        result = json.loads(result)
    except Exception as e:
        try:
            result = REQUEST_CLIENT.cancel_all_orders(symbol=symbol)
            result = json.loads(result)
            print(e)
        except Exception as e:
            try:
                result = REQUEST_CLIENT.cancel_all_orders(symbol=symbol)
                result = json.loads(result)
                print(e)
            except Exception as e:
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("cancelBinanceOrder:"+str(e))


def shortsStopLossByPrice(symbol,stopLossPrice,quantity):
    global FUNCTION_CLIENT,REQUEST_CLIENT,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJMARKET_MAX_SIZE_OBJ,ORDER_ID_INDEX,STOP_LOSS_SYMBOL
    now = int(time.time())
    stopLossResult = True

    stopTime = 5
    stopQuantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (quantity/5)))

    try:
        for i in range(stopTime):
            ORDER_ID_INDEX = ORDER_ID_INDEX+1
            newClientOrderId = "shortsStopLoss_"+STOP_LOSS_SYMBOL+"_"+str(ORDER_ID_INDEX)
            stopLossPrice = float(stopLossPrice)*(1+0.005*i)
            tradePrice =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (stopLossPrice*1.005))
            stopLossPrice =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (stopLossPrice))
            result = REQUEST_CLIENT.post_auto_order_with_price(price=tradePrice,newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=stopQuantity,side=OrderSide.BUY, ordertype=OrderType.STOP, stopPrice=stopLossPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
            result = json.loads(result)
            if "code" in result and str(result["code"])=="4183":
                forceCloseShorts(symbol)
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("code:4183")
        print(result)
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))

    return stopLossResult

def longsStopLossByPrice(symbol,stopLossPrice,quantity):
    global FUNCTION_CLIENT,REQUEST_CLIENT,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJMARKET_MAX_SIZE_OBJ,ORDER_ID_INDEX,STOP_LOSS_SYMBOL
    now = int(time.time())
    stopLossResult = True

    stopTime = 5
    stopQuantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (quantity/5)))

    try:
        for i in range(stopTime):
            ORDER_ID_INDEX = ORDER_ID_INDEX+1
            newClientOrderId = "longsStopLoss_"+STOP_LOSS_SYMBOL+"_"+str(ORDER_ID_INDEX)
            stopLossPrice = float(stopLossPrice)*(1-0.005*i)
            tradePrice =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (stopLossPrice*0.995))
            stopLossPrice =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (stopLossPrice))
            result = REQUEST_CLIENT.post_auto_order_with_price(price=tradePrice,newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=stopQuantity,side=OrderSide.SELL, ordertype=OrderType.STOP, stopPrice=stopLossPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
            result = json.loads(result)
            if "code" in result and str(result["code"])=="4183":
                forceCloseLongs(symbol)
                FUNCTION_CLIENT.send_lark_msg_limit_one_min("code:4183")
            print(result)
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
    return stopLossResult

POSITION_ARR = []

def updatePosition():
    global POSITION_ARR,MACHINE_INDEX
    dataStr = ""
    if MACHINE_INDEX==0:
        dataStr = FUNCTION_CLIENT.get_from_ws_a("E")
    elif MACHINE_INDEX==1:
        print("-----------")
        dataStr = FUNCTION_CLIENT.get_from_ws_b("E")

    dataJson = json.loads(dataStr)

    if dataJson["d"]!="":
        positionStrArr= dataJson["d"].split("&")
        positionArr= []
        for a in range(len(positionStrArr)):
            positionArr.append(positionStrArr[a].split("@"))
            positionArr[a][1] = float(positionArr[a][1])
            positionArr[a][2] = float(positionArr[a][2])
        POSITION_ARR = positionArr
    else:
        POSITION_ARR = []


def getPositionInfoArrBySymbol(symbol):
    global POSITION_ARR
    for positionIndex in range(len(POSITION_ARR)):
        if POSITION_ARR[positionIndex][0] == symbol:
            return [POSITION_ARR[positionIndex][2],POSITION_ARR[positionIndex][1]]
    return [0,0]



DAY_INFO_OBJ = {
    "oneMonthHighPrice":0,
    "oneMonthLowPrice":999999999,
    "oneMonthHighIndex":-1,
    "oneMonthLowIndex":-1,

    "threeDaysHighPrice":0,
    "threeDaysLowPrice":999999999,
    "threeDaysHighIndex":-1,
    "threeDaysLowIndex":-1,

    
    "oneDayHighPrice":0,
    "oneDayLowPrice":999999999,
    "oneDayHighIndex":-1,
    "oneDayLowIndex":-1,
    "oneDayWaveRate":0,

    "updateTs":0
}



def checkAllStopLoss():
    global FUNCTION_CLIENT,POSITION_ARR,PRICE_DECIMAL_OBJ,REQUEST_CLIENT,STOP_LOSS_SYMBOL,DAY_INFO_OBJ

    now = int(time.time()*1000)


    for positionIndex in range(len(POSITION_ARR)):
        errorTime = 0
        while errorTime<3:
            try:
                symbol = POSITION_ARR[positionIndex][0]

                openOrdersResult = REQUEST_CLIENT.get_open_orders(symbol=symbol)
                openOrdersResult = json.loads(openOrdersResult)
                if "code" in openOrdersResult:
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min("checkAllStopLoss ex:"+str(openOrdersResult))
                else:
                    symbolPositionAmt = float(POSITION_ARR[positionIndex][2])
                    symbolCost = float(POSITION_ARR[positionIndex][1])
                    needStopLossValue = symbolPositionAmt*symbolCost

                    if symbolPositionAmt<0:
                        stopLossPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (symbolCost*1.045)))
                        stopAmount = abs(symbolPositionAmt)

                        stopLossOrderIDArr = []
                        allStopLossQuantity = 0
                        stopLossOrderPrice = 0
                        hasStopLossOrder = False
                        for i in range(len(openOrdersResult)):
                            clientOrderId = openOrdersResult[i]['clientOrderId']
                            orderTypeSymbol = clientOrderId.split("_")[0]
                            tradeTypeSymbol = clientOrderId.split("_")[1]
                            if orderTypeSymbol=="shortsStopLoss":
                                stopLossOrderIDArr.append(clientOrderId)
                                allStopLossQuantity = allStopLossQuantity+float(openOrdersResult[i]['origQty'])
                                stopLossOrderPrice = float(openOrdersResult[i]['stopPrice'])

                        if not (abs(allStopLossQuantity)>=abs(symbolPositionAmt*0.95)):
                            stopLossResult = shortsStopLossByPrice(symbol,stopLossPrice,abs(symbolPositionAmt))
                            if stopLossResult:
                                for i in range(len(stopLossOrderIDArr)):
                                    cancelOrder(symbol,stopLossOrderIDArr[i])
                                if len(stopLossOrderIDArr)!=0:
                                    FUNCTION_CLIENT.send_lark_msg_limit_one_min("re stop:"+str(abs(allStopLossQuantity))+","+str(abs(symbolPositionAmt)))
                    elif symbolPositionAmt>0:
                        stopLossPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (symbolCost*0.955)))
                        stopAmount = abs(symbolPositionAmt)

                        stopLossOrderIDArr = []
                        allStopLossQuantity = 0
                        stopLossOrderPrice = 0
                        hasStopLossOrder = False
                        for i in range(len(openOrdersResult)):
                            clientOrderId = openOrdersResult[i]['clientOrderId']
                            orderTypeSymbol = clientOrderId.split("_")[0]
                            tradeTypeSymbol = clientOrderId.split("_")[1]
                            if orderTypeSymbol=="longsStopLoss":
                                stopLossOrderIDArr.append(clientOrderId)
                                allStopLossQuantity = allStopLossQuantity+float(openOrdersResult[i]['origQty'])
                                stopLossOrderPrice = float(openOrdersResult[i]['stopPrice'])
                                if stopLossOrderPrice==stopLossPrice:
                                    hasStopLossOrder = True
                        if not (abs(allStopLossQuantity)>=abs(symbolPositionAmt*0.95)):
                            stopLossResult = longsStopLossByPrice(symbol,stopLossPrice,abs(symbolPositionAmt))
                            if stopLossResult:
                                for i in range(len(stopLossOrderIDArr)):
                                    cancelOrder(symbol,stopLossOrderIDArr[i])
                                if len(stopLossOrderIDArr)!=0:
                                    FUNCTION_CLIENT.send_lark_msg_limit_one_min("re stop:"+str(abs(allStopLossQuantity))+","+str(abs(symbolPositionAmt)))

                errorTime = 10
            except Exception as e:
                ex = traceback.format_exc()
                FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))



SYMBOL_CHECK_TS_OBJ = {}

SQL_UPDATE_TS = 0

ORDER_DATA = ()

CHECK_ALL_STOP_LOSS_TS = 0

while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        now = int(time.time()*1000)
        if now - CHECK_ALL_STOP_LOSS_TS>250:
            CHECK_ALL_STOP_LOSS_TS= now
            updatePosition()
            checkAllStopLoss()
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))