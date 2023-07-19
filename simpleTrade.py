#!/usr/bin/python3.10
# coding=utf-8

import json
import random
import time
import requests
import socket
import decimal
import datetime
import math
import traceback
import _thread
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
import numpy as np
from config import *
from commonFunction import FunctionClient


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="secondOpen")

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

PRIVATE_IP = FUNCTION_CLIENT.get_private_ip()

SERVER_NAME = FUNCTION_CLIENT.getServerName()


BINANCE_API_KEY =""

BINANCE_API_SECRET =""


ORDER_TABLE_NAME = ""


ORDER_ID_SYMBOL = "m"

ORDER_ID_INDEX  = random.randint(1,100000)

TRADE_SYMBOL_ARR =  []

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]

ONE_MIN_KLINE_OBJ_ARR = []

LOCAL_ONE_MIN_KLINE_OBJ_ARR = []


LAST_OPEN_PRICE  = []

LAST_OPEN_RATE_ARR  = []

OPEN_POSITION_TS_ARR  = []

ADD_POSITION_TS_ARR  = []

OPEN_TIME_ARR  = []

TAKE_OPEN_TIME_ARR  = []

LAST_ORDER_INFO_ARR = []

DEPTH_PRICE_ARR = []

OPEN_DIRECTION_ARR  = []

SYMBOL_OPEN_TYPE_ARR = []

SYMBOL_STANDARD_VALUE_ARR = []

SPECIAL_CLOSE_POSITION_ARR = []

POSITION_ARR = []

ACCOUNT_BALANCE_VALUE = 0

BAN_SYMBOL_ARR = []

SYMBOL_STOP_LOSS_TS_ARR = []

LAST_DATA_STR = ""

UPDATE_DATA_STR = False

LAST_DATA_UPDATE_TS = 0

def getTickData():
    global SECOND_NUMBER,ADD_POSITION_TS_ARR,SPECIAL_CLOSE_POSITION_ARR,SYMBOL_STANDARD_VALUE_ARR,SYMBOL_OPEN_TYPE_ARR,SYMBOL_STOP_LOSS_TS_ARR,LAST_DATA_UPDATE_TS,UPDATE_DATA_STR,LAST_DATA_STR,BAN_SYMBOL_ARR,ACCOUNT_BALANCE_VALUE,POSITION_ARR,TAKE_OPEN_TIME_ARR,OPEN_DIRECTION_ARR,LAST_OPEN_PRICE,DEPTH_PRICE_ARR,TRADE_SYMBOL_ARR,FUNCTION_CLIENT,LAST_ORDER_INFO_ARR,OPEN_POSITION_TS_ARR,LAST_OPEN_RATE_ARR,OPEN_TIME_ARR,LOCAL_ONE_MIN_KLINE_OBJ_ARR,ONE_MIN_KLINE_OBJ_ARR,OSS_BUCKET

    now = int(time.time()*1000)
    nowMin = FUNCTION_CLIENT.turn_ts_to_min(now)
    dataStr = ""


    dataStr = FUNCTION_CLIENT.get_from_ws_a("B")


    if now - LAST_DATA_UPDATE_TS>30000:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("dataStr aways equal LAST_DATA_STR",))
    if dataStr!=LAST_DATA_STR:
        UPDATE_DATA_STR = True
        LAST_DATA_UPDATE_TS = now
        LAST_DATA_STR = dataStr
        dataArr = dataStr.split("*")


        ACCOUNT_BALANCE_VALUE = float(dataArr[4])
        if ACCOUNT_BALANCE_VALUE==0:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("ACCOUNT_BALANCE_VALUE==0",))
        if dataArr[3]!="":
            BAN_SYMBOL_ARR = dataArr[3].split("@")
        else:
            BAN_SYMBOL_ARR = []


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



        if len(LOCAL_ONE_MIN_KLINE_OBJ_ARR)>0:
            klineArr = dataArr[0].split("@")
            for a in range(len(klineArr)):
                klineArr[a] = klineArr[a].split("~")
                for b in range(len(klineArr[a])):
                    klineArr[a][b] = klineArr[a][b].split("&")
                    for c in range(len(klineArr[a][b])):
                        klineArr[a][b][c] = float(klineArr[a][b][c])

                    localMin = int(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][4])
                    klineMin = int(klineArr[a][b][0])


                    if localMin == klineMin:
                        ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1] = [klineArr[a][b][1],klineArr[a][b][4],klineArr[a][b][2],klineArr[a][b][3],klineMin]
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = False
                    elif (klineMin == localMin+1) or (klineMin==0 and localMin==59):
                        ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"].append([klineArr[a][b][1],klineArr[a][b][4],klineArr[a][b][2],klineArr[a][b][3],klineMin])
                        del ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][0]
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = False
                    elif  (klineMin < localMin-2) and (localMin!=1 and localMin!=0):
                        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("localMin B:"+str(localMin)+",klineMin:"+str(klineMin)+",symbol:"+str(TRADE_SYMBOL_ARR[a]["symbol"])+","+str(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a]),))
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = True


        priceStrArr= dataArr[1].split("~")
        priceArr= []
        for a in range(len(priceStrArr)):
            priceStrArr[a] = priceStrArr[a].split("^")
            # askPrice  = float(priceStrArr[a][0])
            # bidPrice  = float(priceStrArr[a][1])
            # serverMin  = int(priceStrArr[a][2])
            priceArr.append([float(priceStrArr[a][0]),float(priceStrArr[a][1]),int(priceStrArr[a][2])])

        DEPTH_PRICE_ARR = priceArr

        if len(LOCAL_ONE_MIN_KLINE_OBJ_ARR)!=len(priceArr):
            LOCAL_ONE_MIN_KLINE_OBJ_ARR = []
            for a in range(len(priceArr)):
                serverMin = priceArr[a][2]
                # open close high low

                LOCAL_ONE_MIN_KLINE_OBJ_ARR.append([[priceArr[a][0],priceArr[a][0],priceArr[a][0],priceArr[a][1],serverMin]])
                LAST_OPEN_PRICE.append(0)
                LAST_OPEN_RATE_ARR.append(0)
                OPEN_TIME_ARR.append(0)
                TAKE_OPEN_TIME_ARR.append(0)
                OPEN_DIRECTION_ARR.append("")
                OPEN_POSITION_TS_ARR.append(0)
                SYMBOL_STOP_LOSS_TS_ARR.append(0)
                SYMBOL_OPEN_TYPE_ARR.append("C")
                SYMBOL_STANDARD_VALUE_ARR.append(0)
                ADD_POSITION_TS_ARR.append(0)
                LAST_ORDER_INFO_ARR.append({"highPrice":0,"lowPrice":0})
                SPECIAL_CLOSE_POSITION_ARR.append(False)
        else:
            for a in range(len(priceArr)):

                openPrice = priceArr[a][0]
                closePrice = priceArr[a][1]

                if LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][1]>LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][0]:
                    openPrice = priceArr[a][1]
                    closePrice = priceArr[a][0]
                serverMin = priceArr[a][2]

                localMin = LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][4]

                if localMin == serverMin :
                    if (priceArr[a][0] > LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][2]):
                        LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][2] = priceArr[a][0]
                    
                    if (priceArr[a][1] < LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][3]):
                        LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][3] = priceArr[a][1]

                    LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])-1][1] = closePrice
                elif (localMin+1 == serverMin) or  (localMin==59 and serverMin==0):
                    LOCAL_ONE_MIN_KLINE_OBJ_ARR[a].append([openPrice,closePrice,priceArr[a][0],priceArr[a][1],serverMin])
                else:
                    if localMin-1 != serverMin and  (localMin!=1 and localMin!=0):
                        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("localMin:"+str(localMin)+",serverMin:"+str(serverMin)+",symbol:"+str(TRADE_SYMBOL_ARR[a]["symbol"]),))
                        LOCAL_ONE_MIN_KLINE_OBJ_ARR = []

                if len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a]) > 3:
                    del LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][0]

            for a in range(len(ONE_MIN_KLINE_OBJ_ARR)):
                for b in range(len(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a])):
                    localMin = int(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][4])
                    klineMin = int(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][4])


                    if klineMin == localMin:
                        if LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][2] > ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][2]:
                            ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][2] = LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][2]
                        if LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][3] < ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][3]:
                            ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][3] = LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][3]
                        
                        ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"]) - 1][1] = LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][1]
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = False
                    elif (localMin == klineMin+1) or  (localMin==0 and klineMin==59):
                        ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"].append([LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][0], LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][1], LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][2], LOCAL_ONE_MIN_KLINE_OBJ_ARR[a][b][3],localMin])
                        del ONE_MIN_KLINE_OBJ_ARR[a]["klineArr"][0]
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = False
                    elif localMin < klineMin-2 and  (klineMin!=1 and klineMin!=0):
                        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("localMin A:"+str(localMin)+",klineMin:"+str(klineMin)+",symbol:"+str(TRADE_SYMBOL_ARR[a]["symbol"])+","+str(LOCAL_ONE_MIN_KLINE_OBJ_ARR[a]),))
                        ONE_MIN_KLINE_OBJ_ARR[a]["dataError"] = True


def getOneMinData():
    global ONE_MIN_KLINE_OBJ_ARR,TRADE_SYMBOL_ARR,FUNCTION_CLIENT
    dataStr = FUNCTION_CLIENT.get_from_ws_a("A")
    newKlineDataObjArr = []
    klineArr = dataStr.split("@")


    for a in range(len(klineArr)):
        coin = TRADE_SYMBOL_ARR[a]["coin"]
        quote = TRADE_SYMBOL_ARR[a]["quote"]
        symbol = TRADE_SYMBOL_ARR[a]["symbol"]
        newKlineDataObjArr.append({"coin":coin,"quote":quote,"symbol":symbol,"klineArr":[],"dataError":False})

        klineArr[a] = klineArr[a].split("~")
        for b in range(len(klineArr[a])):
            klineArr[a][b] = klineArr[a][b].split("&")
            for c in range(len(klineArr[a][b])):
                klineArr[a][b][c] = float(klineArr[a][b][c])
            klineMin = int(klineArr[a][b][0])
            newKlineDataObjArr[a]["klineArr"].append([klineArr[a][b][1],klineArr[a][b][4],klineArr[a][b][2],klineArr[a][b][3],klineMin])# open close high low

    if len(newKlineDataObjArr)>0:
        ONE_MIN_KLINE_OBJ_ARR = newKlineDataObjArr




REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY,secret_key=BINANCE_API_SECRET)

PRICE_DECIMAL_OBJ = {}

AMOUNT_DECIMAL_OBJ = {}

PRICE_TICK_OBJ = {}

PRICE_DECIMAL_AMOUNT_OBJ = {}

AMOUNT_DECIMAL_AMOUNT_OBJ = {}

MARKET_MAX_SIZE_OBJ = {}


MARKET_MIN_SIZE_OBJ = {}

def updateSymbolInfo():
    global PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,PRICE_DECIMAL_AMOUNT_OBJ,AMOUNT_DECIMAL_AMOUNT_OBJ,PRICE_TICK_OBJ,MARKET_MAX_SIZE_OBJ,MARKET_MIN_SIZE_OBJ
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
                MARKET_MIN_SIZE_OBJ[thisInstrumentID] = float(symbols[i]['filters'][c]['minQty'])
        PRICE_DECIMAL_OBJ[thisInstrumentID] = priceDecimal
        AMOUNT_DECIMAL_OBJ[thisInstrumentID] = amountDecimal
        PRICE_TICK_OBJ[thisInstrumentID] = priceTick
        PRICE_DECIMAL_AMOUNT_OBJ[thisInstrumentID] = priceDecimalAmount
        if amountDecimalAmount!="":
            AMOUNT_DECIMAL_AMOUNT_OBJ[thisInstrumentID] = int(amountDecimalAmount)

updateSymbolInfo()
while not "BTCUSDT" in PRICE_DECIMAL_OBJ:
    FUNCTION_CLIENT.send_lark_msg_limit_one_min("mainConsole updateSymbolInfo")
    updateSymbolInfo()
    time.sleep(1)


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
                response = requests.request("GET", url,timeout=(1.5,1.5)).json()
            except Exception as e:
                try:
                    url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
                    response = requests.request("GET", url,timeout=(2,2)).json()
                except Exception as e:
                    print(e)
    return response


def getPositionInfoArrBySymbol(symbol):
    global POSITION_ARR
    for positionIndex in range(len(POSITION_ARR)):
        if POSITION_ARR[positionIndex][0] == symbol:
            return [POSITION_ARR[positionIndex][2],POSITION_ARR[positionIndex][1]]
    return [0,0]



def makerShortsOrder(shortsPrice,shortsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_SHORTS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT
    shortsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (shortsPrice)))


    coinQuantity = shortsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        result = REQUEST_CLIENT.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=shortsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTX)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022  and result['code']!=-1001  and result['code']!=-2022:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shorts order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shortsM:"+str(e),))


    return result

def makerCloseLongsOrder(shortsPrice,shortsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_CLOSE_SHORTS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT
    shortsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (shortsPrice)))


    coinQuantity = shortsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "MC_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        result = REQUEST_CLIENT.post_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=coinQuantity,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=shortsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTX)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022  and result['code']!=-1001 and result['code']!=-2022:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("close longs order error:"+str(result)+","+str(coinQuantity)+","+str(symbol),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shortsM:"+str(e),))


    return result


def makerLongsOrder(longsPrice,longsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRIVATE_IP,THIRTY_MINS_POLE_SCORE,RICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_LONGS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT

    longsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (longsPrice)))

    coinQuantity = longsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        result = REQUEST_CLIENT.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=longsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTX)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022 and result['code']!=-1001:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longs order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longsM:"+str(e),))

    return result

def makerCloseShortsOrder(longsPrice,longsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRIVATE_IP,THIRTY_MINS_POLE_SCORE,RICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_CLOSE_LONGS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT

    longsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (longsPrice)))

    coinQuantity = longsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = "MC_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        result = REQUEST_CLIENT.post_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=coinQuantity,side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=longsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTX)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022 and result['code']!=-1001 and result['code']!=-2022:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("close shorts order error:"+str(result)+","+str(coinQuantity)+","+str(symbol),))

        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longsM:"+str(e),))

    return result


BALANCE_WARN_TS = 0

ONCE_TRADE_VALUE = 0


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

LAST_NEW_OPEN_TS = 0

LAST_UPDATE_TRADE_STATUS_TS = 0

UPDATE_ONE_DAY_RATE_TS = 0

SYMBOL_STOP_TRADE_WARN_TS_OBJ = {}

RUN_TIME = 0

BIG_LOSS_LIMIT_TS = 0


STANDARD_TRADE_VALUE = 1000


UPDATE_VOL_TS = 0

STOP_OPEN_LONGS_BY_TOO_MANY_FIT_TS = 0

STOP_OPEN_SHORTS_BY_TOO_MANY_FIT_TS = 0

UPDATE_ACCOUNT_BALANCE_VALUE_TS = 0

BTC_NOW_OPEN_RATE  = 0

ETH_NOW_OPEN_RATE  = 0

SPECIAL_MODE = False

def newOpenOrders():
    global SPECIAL_MODE,ETH_NOW_OPEN_RATE,BTC_NOW_OPEN_RATE,SECOND_NUMBER,SEND_POSITION_TS,MARKET_MIN_SIZE_OBJ,STANDARD_TRADE_VALUE,ADD_POSITION_TS_ARR,SPECIAL_CLOSE_POSITION_ARR,CONDITION_AND_RATE_ARR_A,CONDITION_AND_RATE_ARR_B,SYMBOL_STANDARD_VALUE_ARR,SYMBOL_OPEN_TYPE_ARR,BAN_SYMBOL_ARR,UPDATE_ACCOUNT_BALANCE_VALUE_TS,MULTIPLE_OBJ_B,MULTIPLE_OBJ_A,STOP_OPEN_SHORTS_BY_TOO_MANY_FIT_TS,STOP_OPEN_LONGS_BY_TOO_MANY_FIT_TS,UPDATE_VOL_CONDITION_A,UPDATE_VOL_CONDITION_B,UPDATE_VOL_TS,STANDARD_TRADE_VALUE,BIG_LOSS_LIMIT_TS,FOUR_HOURS_VOL_OBJ_A,THREE_DAYS_VOL_OBJ_A,LAST_OPEN_PRICE,SECOND_NUMBER,RUN_TIME,SYMBOL_STOP_TRADE_WARN_TS_OBJ,SYMBOL_STOP_LOSS_TS_ARR,UPDATE_ONE_DAY_RATE_TS,DEPTH_PRICE_ARR,LAST_UPDATE_TRADE_STATUS_TS,ACCOUNT_BALANCE_VALUE,FUNCTION_CLIENT,ONCE_TRADE_VALUE,PUBLIC_SERVER_IP,LAST_NEW_OPEN_TS,FILL_WARN_TS,POSITION_ARR,LAST_ORDER_INFO_ARR,OPEN_POSITION_TS_ARR,OPEN_DIRECTION_ARR,TAKE_OPEN_TIME_ARR,OPEN_TIME_ARR,LAST_OPEN_RATE_ARR,NEW_OPEN_CLASS,MARKET_MIN_SIZE_OBJ,ONE_HOUR_POLE_SCORE,THIRTY_MINS_POLE_SCORE,NEED_CANCEL_SHORTS_ORDER_ID_ARR,NEED_CANCEL_LONGS_ORDER_ID_ARR,AMOUNT_DECIMAL_AMOUNT_OBJ,LAST_LONGS_ORDER_TS,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,AMOUNT_DECIMAL_OBJ,DATA_DELAY_WARN_TS,NEED_CANCEL_SHORTS_ORDER_ID_ARR,ONE_HOUR_CLOSE_OBJ_ARR,ONE_HOUR_POLE_OBJ,UPDATE_ONE_HOUR_POLE_OBJ_TS,MAKER_COMMISSION_RATE,UPDATE_THIRTY_MINS_POLE_OBJ_TS,THIRTY_MINS_POLE_OBJ,THIRTY_MINS_CLOSE_OBJ_ARR,STOP_SERVER_WARN_TS,DAY_INFO_OBJ,CLOSE_OBJ_ARR,TRADE_INFO,ORDER_TABLE_NAME,START_TRADE_TS,NOW_POSITION_AMOUNT,END_TRADE_TS,LAST_OPEN_MID_PRICE,NEED_CANCEL_LONGS_ORDER_ID_ARR,SHORTS_DEPTH_CHANGE_RATE,LONGS_DEPTH_CHANGE_RATE,PRIVATE_IP,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT

    now = int(time.time()*1000)

    allProfit  = 0
    for oneMinKlineObjArrIndex in range(len(ONE_MIN_KLINE_OBJ_ARR)):

        symbol = ONE_MIN_KLINE_OBJ_ARR[oneMinKlineObjArrIndex]["symbol"]

        symbolPositionInfoArr = getPositionInfoArrBySymbol(symbol)
        positionCost = symbolPositionInfoArr[1]
        symbolPositionAmt = symbolPositionInfoArr[0]
        positionValue = abs(positionCost*symbolPositionAmt)
        oneMinArr = ONE_MIN_KLINE_OBJ_ARR[oneMinKlineObjArrIndex]["klineArr"]
        dataError = ONE_MIN_KLINE_OBJ_ARR[oneMinKlineObjArrIndex]["dataError"]

        nowOpenPrice = float(oneMinArr[len(oneMinArr)-1][0])
        nowClosePrice =float(oneMinArr[len(oneMinArr)-1][1])
        nowHighPrice = float(oneMinArr[len(oneMinArr)-1][2])
        nowLowPrice = float(oneMinArr[len(oneMinArr)-1][3])

        allProfit = allProfit+symbolPositionAmt*(float(oneMinArr[len(oneMinArr)-1][1])-positionCost)

        openQuantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (100/nowClosePrice )))
        closeQuantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (100/nowClosePrice )))
        oneMinsRate = FUNCTION_CLIENT.get_percent_num(float(oneMinArr[len(oneMinArr)-1][1])-float(oneMinArr[len(oneMinArr)-1-1][1]),float(oneMinArr[len(oneMinArr)-1-1][1]))

        #一分钟下跌超过1%，并且该币种没有仓位则开多
        if oneMinsRate<-1 and positionValue==0:
            result = makerLongsOrder(nowClosePrice,openQuantity,symbol)
            errorTime = 1
            while ('code' in result and (result['code'] ==-5022 or result['code'] ==-1001)):
                result = makerLongsOrder(nowClosePrice,openQuantity,symbol)
                errorTime = errorTime+1
                getTickData()
        #一分钟上涨超过0.5%，并且该币种没有仓位则平多
        if oneMinsRate>0.5 and positionValue!=0:
            result = makerCloseLongsOrder(nowClosePrice,closeQuantity,symbol)
            errorTime = 1
            while ('code' in result and (result['code'] ==-5022 or result['code'] ==-1001)):
                result = makerCloseLongsOrder(shortsPriceObj["price"],closeQuantity,symbol)
                errorTime = errorTime+1
                if errorTime>3:
                    _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg,(" errorTime>3 A:"+symbol,))
                    time.sleep(errorTime*0.1)
            LAST_ORDER_INFO_ARR[oneMinKlineObjArrIndex]["highPrice"] = nowHighPrice

    #当前持仓总利润低于-100则强制平仓

    if allProfit<=-100:
        for i in range(len(POSITION_ARR)):
            if POSITION_ARR[i][2]<0:
                _thread.start_new_thread( forceCloseShorts, (POSITION_ARR[i][0],) )
            if POSITION_ARR[i][2]>0:
                _thread.start_new_thread( forceCloseLongs, (POSITION_ARR[i][0],) )
        FUNCTION_CLIENT.send_lark_msg_limit_one_min("allProfit<=-100:"+str(allProfit))

getOneMinData()
getTickData()

GET_ONE_MIN_DATA_TS = 0

print("begin")

while 1:
    now = int(time.time()*1000)
    try:
        if now - GET_ONE_MIN_DATA_TS>60*1000:
            GET_ONE_MIN_DATA_TS  = now
            getOneMinData()
        getTickData()
        if UPDATE_DATA_STR:
            UPDATE_DATA_STR = False
            newOpenOrders()
        RUN_TIME = RUN_TIME+1
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        print(e)
        print(ex)
        time.sleep(1)