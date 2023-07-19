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
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
ORDER_ID_SYMBOL = "t"


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="checkTimeoutOrders",connectMysql =True)


SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("checkTimeoutOrders_",""))

BINANCE_API_KEY_ARR =["",""]
BINANCE_API_SECRET_ARR =["",""]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])


PRIVATE_IP = FUNCTION_CLIENT.get_private_ip()

ORDER_ID_INDEX  = random.randint(1,100000)


SERVER_IP_ARR = []
nowPage =1
emptyReq =False
while  not emptyReq:
    client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
    client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
    request = DescribeInstancesRequest()
    request.set_PageNumber(nowPage)
    request.set_PageSize(100)
    request.set_accept_format('json')
    # request.modify_point('cn-hongkong','ecs',"ecs.cn-hongkong.aliyuncs.com")
    # request.set_Endpoint("ecs.cn-hongkong.aliyuncs.com")
    instanceInfoArr = client.do_action_with_exception(request)
    instanceInfoArr=json.loads(str(instanceInfoArr, encoding='utf-8'))

    instanceInfoArr=instanceInfoArr["Instances"]["Instance"]
    if len(instanceInfoArr)==0:
        emptyReq=True
    else:
        for i in range(len(instanceInfoArr)):
            if instanceInfoArr[i]["InstanceName"].find("secondOpen")>=0:
                print(instanceInfoArr[i]["InstanceName"])
                machineNumber  = int(instanceInfoArr[i]["InstanceName"].split("_")[1])
                if MACHINE_INDEX==0 and machineNumber<=6:
                    SERVER_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if MACHINE_INDEX==1 and machineNumber>6:
                    SERVER_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
    nowPage = nowPage+1

SERVER_IP_ARR_INDEX = 0

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
    FUNCTION_CLIENT.send_lark_msg("mainConsole updateSymbolInfo")
    updateSymbolInfo()
    time.sleep(1)



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



def takeShortsOrderA(shortsPrice,shortsOnceTradeCoinQuantity,symbol):
    global REQUEST_CLIENT,FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_SHORTS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT
    shortsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (shortsPrice)))

    coinQuantity = shortsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_T_"+str(ORDER_ID_INDEX)
    result = {}
    try:

        requestClient = RequestClient(api_key=BINANCE_API_KEY_ARR[0],secret_key=BINANCE_API_SECRET_ARR[0])
        result = requestClient.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=shortsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022  and result['code']!=-1001  and result['code']!=-2022:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shorts order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shortsM:"+str(e),))


    return result


def takeLongsOrderA(longsPrice,longsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRIVATE_IP,THIRTY_MINS_POLE_SCORE,RICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_LONGS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT

    longsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (longsPrice)))

    coinQuantity = longsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_T_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        requestClient = RequestClient(api_key=BINANCE_API_KEY_ARR[0],secret_key=BINANCE_API_SECRET_ARR[0])
        result = requestClient.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=longsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022 and result['code']!=-1001:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longs order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longsM:"+str(e),))

    return result

def takeShortsOrderB(shortsPrice,shortsOnceTradeCoinQuantity,symbol):
    global REQUEST_CLIENT,FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_SHORTS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT
    shortsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (shortsPrice)))

    coinQuantity = shortsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_T_"+str(ORDER_ID_INDEX)
    result = {}
    try:

        requestClient = RequestClient(api_key=BINANCE_API_KEY_ARR[1],secret_key=BINANCE_API_SECRET_ARR[1])
        result = requestClient.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=shortsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022  and result['code']!=-1001  and result['code']!=-2022:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shorts order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("shortsM:"+str(e),))


    return result


def takeLongsOrderB(longsPrice,longsOnceTradeCoinQuantity,symbol):
    global FUNCTION_CLIENT,ORDER_ID_SYMBOL,PRICE_MOVE_SYMBOL,PRIVATE_IP,PUBLIC_SERVER_IP,SEND_PUBLIC_SERVER_TS,PRIVATE_IP,THIRTY_MINS_POLE_SCORE,RICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,ORDER_ID_INDEX,REQUEST_CLIENT,NEED_CANCEL_LONGS_ORDER_ID_ARR,TRADE_INFO,EIGHT_HOURS_PROFIT,TRADE_INFO,FOUR_HOURS_PROFIT,EIGHT_HOURS_PROFIT,TWELVE_HOURS_PROFIT,TWENTY_FOUR_HOURS_PROFIT

    longsPrice = float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (longsPrice)))

    coinQuantity = longsOnceTradeCoinQuantity

    ORDER_ID_INDEX = ORDER_ID_INDEX+1
    newClientOrderId = ORDER_ID_SYMBOL+"_T_"+str(ORDER_ID_INDEX)
    result = {}
    try:
        requestClient = RequestClient(api_key=BINANCE_API_KEY_ARR[1],secret_key=BINANCE_API_SECRET_ARR[1])
        result = requestClient.post_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=longsPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        if "code" in result and result['code']!=-5022 and result['code']!=-1001:
            _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longs order error:"+str(result)+","+str(coinQuantity),))
        print("--------------")
        print(result)
    except Exception as e:
        _thread.start_new_thread(FUNCTION_CLIENT.send_lark_msg_limit_one_min,("longsM:"+str(e),))

    return result

def getFutureDepthBySymbol(symbol,limit):
    response = {}
    try:
        url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit=50"
        response = requests.request("GET", url,timeout=(0.5,0.5)).json()
    except Exception as e:
        try:
            url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit=50"
            response = requests.request("GET", url,timeout=(1,1)).json()
        except Exception as e:
            try:
                url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit=50"
                response = requests.request("GET", url,timeout=(2,2)).json()
            except Exception as e:
                print(e)
    return response



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

LAST_CHECK_TIME_OUT_ORDERS_TS = 0

TAKE_ORDERS_OBJ_ARR_A = []

TAKE_ORDERS_OBJ_ARR_B = []

#{"ts":0,"makeClientOrderId":"","status":"wait or finish"}
def checkTimeoutOrders():
    global REQUEST_CLIENT,LAST_CHECK_TIME_OUT_ORDERS_TS,TAKE_ORDERS_OBJ_ARR_A,TAKE_ORDERS_OBJ_ARR_B,SERVER_IP_ARR,SERVER_IP_ARR_INDEX,BINANCE_API_KEY_ARR,BINANCE_API_SECRET_ARR,MACHINE_INDEX
    now = int(time.time()*1000)
    if now - LAST_CHECK_TIME_OUT_ORDERS_TS>=500:
        LAST_CHECK_TIME_OUT_ORDERS_TS = now
        # result = REQUEST_CLIENT.get_all_open_orders()
        SERVER_IP_ARR_INDEX = SERVER_IP_ARR_INDEX+1
        if SERVER_IP_ARR_INDEX>=len(SERVER_IP_ARR):
            SERVER_IP_ARR_INDEX = 0
        PUBLIC_SERVER_IP = "http://"+SERVER_IP_ARR[SERVER_IP_ARR_INDEX]+":8888/"
        postDataObj = {'key':BINANCE_API_KEY_ARR[MACHINE_INDEX],'secret':BINANCE_API_SECRET_ARR[MACHINE_INDEX] }
        result = requests.request("POST", PUBLIC_SERVER_IP+"get_all_open_orders", timeout=3,data=postDataObj).json()
        openOrdersResult = result["r"]
        print(openOrdersResult)
        if "code" in result:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(result))
        else:
            openTakeObjA = {}
            openTakeObjB = {}
            for a in range(len(openOrdersResult)):
                clientOrderId = openOrdersResult[a]['clientOrderId']
                orderOpenTime = openOrdersResult[a]['time']
                symbol = openOrdersResult[a]['symbol']
                side = openOrdersResult[a]['side']
                origQty = abs(float(openOrdersResult[a]['origQty']))
                orderPrice = float(openOrdersResult[a]['price'])
                orderValue = origQty*orderPrice
                direction = "shorts"
                if side =="BUY":
                    direction = "longs"
                orderTypeSymbol = ""
                tradeTypeSymbol = ""
                try:
                    orderTypeSymbol = clientOrderId.split("_")[0]
                    tradeTypeSymbol = clientOrderId.split("_")[1]
                except Exception as e:
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(clientOrderId))
                    _thread.start_new_thread( FUNCTION_CLIENT.cancel_binance_order_by_web_server, (symbol,BINANCE_API_KEY_ARR[MACHINE_INDEX],BINANCE_API_SECRET_ARR[MACHINE_INDEX],clientOrderId, ) )
                print(orderTypeSymbol)

                symbolPositionInfoArr = getPositionInfoArrBySymbol(symbol)
                positionCost = symbolPositionInfoArr[1]
                symbolPositionAmt = symbolPositionInfoArr[0]
                if (orderTypeSymbol=="shortsStopLoss") and positionCost==0:
                    _thread.start_new_thread( FUNCTION_CLIENT.cancel_binance_order_by_web_server, (symbol,BINANCE_API_KEY_ARR[MACHINE_INDEX],BINANCE_API_SECRET_ARR[MACHINE_INDEX],clientOrderId, ) )
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min("cancel shortsStopLoss by position ==0")
                if (orderTypeSymbol=="longsStopLoss") and positionCost==0:
                    _thread.start_new_thread( FUNCTION_CLIENT.cancel_binance_order_by_web_server, (symbol,BINANCE_API_KEY_ARR[MACHINE_INDEX],BINANCE_API_SECRET_ARR[MACHINE_INDEX],clientOrderId, ) )
                    FUNCTION_CLIENT.send_lark_msg_limit_one_min("cancel longsStopLoss by position ==0")
                if (orderTypeSymbol=="wTake") and now -orderOpenTime>1*15*1000:
                    _thread.start_new_thread( FUNCTION_CLIENT.cancel_binance_order_by_web_server, (symbol,BINANCE_API_KEY_ARR[MACHINE_INDEX],BINANCE_API_SECRET_ARR[MACHINE_INDEX],clientOrderId, ) )

                if (orderTypeSymbol=="MC") and now -orderOpenTime>1*60*1000:
                    _thread.start_new_thread( FUNCTION_CLIENT.cancel_binance_order_by_web_server, (symbol,BINANCE_API_KEY_ARR[MACHINE_INDEX],BINANCE_API_SECRET_ARR[MACHINE_INDEX],clientOrderId, ) )
                if orderValue>100 and orderTypeSymbol=="m" and now -orderOpenTime>=2.5*1000 and now -orderOpenTime<1*60*1000:
                    takeOrdersObjArrIndex = -1
                    hasTake = False
                    for b in range(len(TAKE_ORDERS_OBJ_ARR_A)):
                        if TAKE_ORDERS_OBJ_ARR_A[b]["makeClientOrderId"]==clientOrderId:
                            hasTake = True

                    if not hasTake:
                        TAKE_ORDERS_OBJ_ARR_A.append({"ts":now,"makeClientOrderId":clientOrderId})
                        if symbol in openTakeObjA:
                            openTakeObjA[symbol]["quantity"] = openTakeObjA[symbol]["quantity"]+origQty*0.3
                        else:
                            openTakeObjA[symbol]={"quantity":origQty*0.3,"direction":direction}

                if MACHINE_INDEX==0 and orderValue>100 and (orderTypeSymbol=="m" or orderTypeSymbol=="t") and now -orderOpenTime>=5*1000 and now -orderOpenTime<1*60*1000:
                    takeOrdersObjArrIndex = -1
                    hasTake = False
                    for b in range(len(TAKE_ORDERS_OBJ_ARR_B)):
                        if TAKE_ORDERS_OBJ_ARR_B[b]["makeClientOrderId"]==clientOrderId:
                            hasTake = True

                    if not hasTake:
                        TAKE_ORDERS_OBJ_ARR_B.append({"ts":now,"makeClientOrderId":clientOrderId})
                        if symbol in openTakeObjB:
                            openTakeObjB[symbol]["quantity"] = openTakeObjB[symbol]["quantity"]+origQty*0.3
                        else:
                            openTakeObjB[symbol]={"quantity":origQty*0.3,"direction":direction}

            # if MACHINE_INDEX==0:
            #     for key in openTakeObjA:
            #         depthArr = getFutureDepthBySymbol(key,50)
            #         asksDepthArr = depthArr["asks"]
            #         bidsDepthArr = depthArr["bids"]
            #         nowPrice = (float(depthArr["bids"][0][0])+float(depthArr["asks"][0][0]))/2
            #         quantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[key] % (openTakeObjA[key]["quantity"] )))
            #         if openTakeObjA[key]["direction"]=="longs":
            #             ordersResult = takeLongsOrderA(float(depthArr["bids"][0][0])*1.002,quantity,key)
            #         if openTakeObjA[key]["direction"]=="shorts":
            #             ordersResult = takeShortsOrderA(float(depthArr["asks"][0][0])*0.998,quantity,key)
            #         updateSql = "update trades set `takeTime` = `takeTime`+1,`takeValue` = `takeValue`+%s where symbol=%s and status='tradeBegin'"
            #         FUNCTION_CLIENT.mysql_commit(updateSql,[quantity*nowPrice,key])


            #     for key in openTakeObjB:
            #         depthArr = getFutureDepthBySymbol(key,50)
            #         asksDepthArr = depthArr["asks"]
            #         bidsDepthArr = depthArr["bids"]
            #         nowPrice = (float(depthArr["bids"][0][0])+float(depthArr["asks"][0][0]))/2
            #         quantity = float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[key] % (openTakeObjB[key]["quantity"] )))
            #         if openTakeObjB[key]["direction"]=="longs":
            #             ordersResult = takeLongsOrderB(float(depthArr["bids"][0][0])*1.002,quantity,key)
            #         if openTakeObjB[key]["direction"]=="shorts":
            #             ordersResult = takeShortsOrderB(float(depthArr["asks"][0][0])*0.998,quantity,key)

            #     for a in range(len(TAKE_ORDERS_OBJ_ARR_A)):
            #         if now - TAKE_ORDERS_OBJ_ARR_A[a]["ts"]>3*60000:
            #             TAKE_ORDERS_OBJ_ARR_A.remove(TAKE_ORDERS_OBJ_ARR_A[a])
            #             break

            #     for a in range(len(TAKE_ORDERS_OBJ_ARR_B)):
            #         if now - TAKE_ORDERS_OBJ_ARR_B[a]["ts"]>3*60000:
            #             TAKE_ORDERS_OBJ_ARR_B.remove(TAKE_ORDERS_OBJ_ARR_B[a])
            #             break
while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        updatePosition()
        checkTimeoutOrders()
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(3)
        print(e)
        print(ex)