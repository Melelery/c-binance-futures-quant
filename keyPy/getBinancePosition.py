#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果
import json
import random
import time
import requests
import socket
import decimal
import traceback
import _thread
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="getBinancePosition",connectMysql =True)

privateIP = FUNCTION_CLIENT.get_private_ip()

sql = "select `symbol`,`id`,`index` from trade_symbol where `status`='yes' order by id asc" 
TRADE_SYMBOL_DATA = FUNCTION_CLIENT.mysql_select(sql,[])

TRADE_SYMBOL_ARR = []
for i in range(len(TRADE_SYMBOL_DATA)):
    symbolIndex = str(TRADE_SYMBOL_DATA[i][2])
    if len(symbolIndex) ==2:
        symbolIndex = "0"+symbolIndex
    if len(symbolIndex) ==1:
        symbolIndex = "00"+symbolIndex
    TRADE_SYMBOL_ARR.append({
            "symbol":TRADE_SYMBOL_DATA[i][0],
            "id":TRADE_SYMBOL_DATA[i][1],
            "price":"0",
            "symbolIndex":symbolIndex,
            "positionIndex":0
        })


SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("getBinancePosition_",""))

BINANCE_API_KEY_ARR =[""]
BINANCE_API_SECRET_ARR =[""]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])



INFO_ARR = {"positionArr":[],"balance":-999999999,"eightHoursProfit":0,"fourHoursProfit":0,"twelveHoursProfit":0,"twentyFourHoursProfit":0,"profit":{},"commission":{}}


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

BNB_PRICE  = 0
LAST_UPDATE_BNB_PRICE_TS = 0
def updateBnbPrice():
    global BNB_PRICE,LAST_UPDATE_BNB_PRICE_TS
    now  = int(time.time()*1000)
    if now - LAST_UPDATE_BNB_PRICE_TS>60000:
        LAST_UPDATE_BNB_PRICE_TS = now
        try:
            url = "https://fapi.binance.com/fapi/v1/klines?symbol=BNBUSDT&limit=1&interval=1m"
            response = requests.request("GET", url,timeout=(2,2)).json()
            if float(response[0][4])>0:
                BNB_PRICE = float(response[0][4])
        except Exception as e:
            print(e)


def getBinancePosition():
    global BINANCE_API_KEY_ARR,MACHINE_INDEX,REQUEST_CLIENT,TRADE_SYMBOL_ARR,BNB_PRICE,FUNCTION_CLIENT,INFO_ARR,COST,COIN_BALANCE,BINANCE_API_KEY,BINANCE_API_SECRET,INSTRUMENT_ID,COIN,UPDATE_BINANCE_POSITION_DELAY_WARN_TS,UNREALIZED_PROFIT,NOW_OPEN_POSITION_COIN_AMOUNT,SYMBOL
    now = int(time.time()*1000)
    result = REQUEST_CLIENT.get_account_information()
    result = json.loads(result)
    if "code" in result:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min("getBinancePosition code:"+str(result))
    else:
        positionsArr = result["positions"]
        assetsArr = result["assets"]
        INFO_ARR["positionArr"] = []
        INFO_ARR["assetsArr"] = assetsArr
        INFO_ARR["balance"] = 0

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

        assetsUpdateTs = 0
        for i in range(len(assetsArr)):
            if assetsArr[i]['updateTime']>assetsUpdateTs:
                assetsUpdateTs = assetsArr[i]['updateTime']
            if assetsArr[i]['asset'] == "USDT":
                INFO_ARR["balance"] = INFO_ARR["balance"]+float(assetsArr[i]['marginBalance'])
            if assetsArr[i]['asset'] == "BUSD":
                INFO_ARR["balance"] = INFO_ARR["balance"]+float(assetsArr[i]['marginBalance'])
            if assetsArr[i]['asset'] == "BNB":
                INFO_ARR["balance"] = INFO_ARR["balance"]+float(assetsArr[i]['marginBalance'])*BNB_PRICE

        if MACHINE_INDEX==0:
            if positionUpdateTs>0:
                sendStr = "gggoihsoaitowljd"+str(positionUpdateTs)+sendStr
                FUNCTION_CLIENT.send_to_ws_a(sendStr)
            if assetsUpdateTs>0:
                sendStr = "fdsoihsoaitowljd"+str(assetsUpdateTs)+str(int(INFO_ARR["balance"]))
                FUNCTION_CLIENT.send_to_ws_a(sendStr)

        elif MACHINE_INDEX==1:
            if positionUpdateTs>0:
                sendStr = "gggoihsoaitowljd"+str(positionUpdateTs)+sendStr
                FUNCTION_CLIENT.send_to_ws_b(sendStr)
            if assetsUpdateTs>0:
                sendStr = "fdsoihsoaitowljd"+str(assetsUpdateTs)+str(int(INFO_ARR["balance"]))
                FUNCTION_CLIENT.send_to_ws_b(sendStr)

        inputData= json.dumps(INFO_ARR)

        with open('/var/www/html/'+BINANCE_API_KEY_ARR[MACHINE_INDEX][0:10]+'.json', 'w',encoding='UTF-8') as fp:
            fp.write(inputData)
            fp.close()



while 1:
    try:
        _thread.start_new_thread(FUNCTION_CLIENT.update_machine_status,())
        _thread.start_new_thread(updateBnbPrice,())
        getBinancePosition()
        time.sleep(0.1)
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        time.sleep(1)