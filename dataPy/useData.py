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


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="useData")

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

LAST_DATA_UPDATE_TS = 0

UPDATE_DATA_STR  = False

LAST_DATA_STR = ""

BAN_SYMBOL_ARR = []

ACCOUNT_BALANCE_VALUE = 0

POSITION_ARR = []

DEPTH_PRICE_ARR = []


TRADE_SYMBOL_ARR =  []

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]

LOCAL_ONE_MIN_KLINE_OBJ_ARR = []

ONE_MIN_KLINE_OBJ_ARR = []


def getTickData():
    global LAST_DATA_UPDATE_TS,UPDATE_DATA_STR,LAST_DATA_STR,BAN_SYMBOL_ARR,ACCOUNT_BALANCE_VALUE,POSITION_ARR,DEPTH_PRICE_ARR,TRADE_SYMBOL_ARR,FUNCTION_CLIENT,LOCAL_ONE_MIN_KLINE_OBJ_ARR,ONE_MIN_KLINE_OBJ_ARR

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


getOneMinData()

getTickData()

for i in range(len(ONE_MIN_KLINE_OBJ_ARR)):
	print("symbol:"+ONE_MIN_KLINE_OBJ_ARR[i]["symbol"])
	print("now open price:"+str(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"])-1][0]))
	print("now close price:"+str(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"])-1][1]))
	print("now high price:"+str(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"])-1][2]))
	print("now low price:"+str(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"][len(ONE_MIN_KLINE_OBJ_ARR[i]["klineArr"])-1][3]))