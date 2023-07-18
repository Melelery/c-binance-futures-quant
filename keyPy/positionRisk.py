#!/usr/bin/python3.10
# coding=utf-8
import _thread
import json
import random
import time
import requests
import socket
import decimal
import traceback
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="positionRisk",connectMysql =True)

privateIP = FUNCTION_CLIENT.get_private_ip()

SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("positionRisk_",""))


BINANCE_API_KEY_ARR =["WqGYwxXHwYgTmBK9jpDeuFvpGTPpclQSGKAez1aMEAUt7ME8R9qsIktdtxrKTc6Q","lhXbl1CZj6Wm7euIxuAXjfZTfXapLcWxhcejamWVUY0kVjcqJ8nwJHeusQfKjnBL"]
BINANCE_API_SECRET_ARR =["LLLhzRFM6hFoaYdOZl3pSTsxKGuMKdIFto66mf9y83j8xPx7wvGe4f6lycqIsFNC","XA41gp9z2lvFu4YysJn5CPQ8NqJnlxHlx8Fl1LjIxNOj2xIDFjxRCK7cK5RbRsfG"]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])


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



def getOKExFutureDepthBySymbol(symbol):
    response = {}
    instId = ""
    if symbol=="BTCUSDT":
        instId = "BTC-USDT-SWAP"
    if symbol=="ETHUSDT":
        instId = "ETH-USDT-SWAP"
    price = 0
    try:
        url = "https://www.okx.com/api/v5/market/books?instId="+instId
        response = requests.request("GET", url,timeout=(0.5,0.5)).json()
        price = (float(response["data"][0]["asks"][0][0]) +float(response["data"][0]["bids"][0][0]))/2
    except Exception as e:
        try:
            url = "https://www.okx.com/api/v5/market/books?instId="+instId
            response = requests.request("GET", url,timeout=(0.5,0.5)).json()
            price = (float(response["data"][0]["asks"][0][0]) +float(response["data"][0]["bids"][0][0]))/2
        except Exception as e:
            try:
                url = "https://www.okx.com/api/v5/market/books?instId="+instId
                response = requests.request("GET", url,timeout=(0.5,0.5)).json()
                price = (float(response["data"][0]["asks"][0][0]) +float(response["data"][0]["bids"][0][0]))/2
            except Exception as e:
                print(e)
    return price


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


def forceCloseShorts(symbol):
    global FUNCTION_CLIENT,REQUEST_CLIENT,ORDER_ID_INDEX,MARKET_MAX_SIZE_OBJ

    marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseShorts_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.BUY, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if 'code' in result:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min("force code:"+str(result))
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
    global FUNCTION_CLIENT,REQUEST_CLIENT,ORDER_ID_INDEX,MARKET_MAX_SIZE_OBJ

    marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseLongs_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.SELL, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if 'code' in result:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(" force code:"+str(result))
        print(result)
    except Exception as e:
        print(e)
    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "forceCloseLongs_c_"+str(ORDER_ID_INDEX)
    try:
        result = REQUEST_CLIENT.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side= OrderSide.SELL, ordertype=OrderType.MARKET, price="0", positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        print(result)
    except Exception as e:
        print(e)



INFO_ARR = {"positionArr":[],"balance":-999999999,"eightHoursProfit":0,"fourHoursProfit":0,"twelveHoursProfit":0,"twentyFourHoursProfit":0,"profit":{},"commission":{}}

def getBinancePosition():
    global REQUEST_CLIENT,FUNCTION_CLIENT,INFO_ARR,COST,COIN_BALANCE,INSTRUMENT_ID,COIN,UPDATE_BINANCE_POSITION_DELAY_WARN_TS,UNREALIZED_PROFIT,NOW_OPEN_POSITION_COIN_AMOUNT,DELAY_ERROR_SEND_TS_A,DELAY_ERROR_SEND_TS_B
    now = int(time.time()*1000)
    result = REQUEST_CLIENT.get_position()
    result = json.loads(result)
    if "code" in result:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min("getBinancePosition ex:"+str(result))
    else:
        INFO_ARR["positionArr"] = []
        for i in range(len(result)):

            if float(result[i]["entryPrice"])!=0:
                symbol = str(result[i]["symbol"])
                stopLossRate = 7
                positionAmt = float(result[i]["positionAmt"])
                entryPrice =  float(result[i]["entryPrice"])
                depthObj = getFutureDepthBySymbol(symbol,5)

                binancePrice = (float(depthObj["asks"][0][0])+float(depthObj["bids"][0][0]))/2

                if positionAmt<0:
                    if binancePrice>entryPrice*(1+stopLossRate/100):
                        forceCloseShorts(symbol)
                        FUNCTION_CLIENT.send_lark_msg_limit_one_min("forceCloseShorts")
                if positionAmt>0:
                    if binancePrice<entryPrice*(1-stopLossRate/100):
                        forceCloseLongs(symbol)
                        FUNCTION_CLIENT.send_lark_msg_limit_one_min("forceCloseLongs")
            INFO_ARR["positionArr"].append(result[i])

        positionsArr =result
        sendStr = ""
        positionUpdateTs = 0
        for a in range(len(positionsArr)):
            if float(positionsArr[a]["entryPrice"])!=0:
                if positionsArr[a]["updateTime"]>positionUpdateTs:
                    positionUpdateTs = positionsArr[a]["updateTime"]
                INFO_ARR["positionArr"].append(positionsArr[a])
                if sendStr=="":
                    sendStr = positionsArr[a]["symbol"]+"@"+positionsArr[a]["entryPrice"]+"@"+positionsArr[a]["positionAmt"]
                else:
                    sendStr = sendStr+"&"+positionsArr[a]["symbol"]+"@"+positionsArr[a]["entryPrice"]+"@"+positionsArr[a]["positionAmt"]



while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        getBinancePosition()
        time.sleep(0.1)
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(1)