#!/usr/bin/python3.10
# coding=utf-8
import websocket
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

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="wsPosition",connectMysql =True)

SERVER_NAME = FUNCTION_CLIENT.getServerName()

MACHINE_INDEX = int(SERVER_NAME.replace("wsPosition_",""))

BINANCE_API_KEY_ARR =["",""]
BINANCE_API_SECRET_ARR =["",""]

REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[MACHINE_INDEX],secret_key=BINANCE_API_SECRET_ARR[MACHINE_INDEX])

LISTEN_KEY = ""
def updateKey():
    global LISTEN_KEY,REQUEST_CLIENT
    try:
        result = REQUEST_CLIENT.get_listen_key()
        result = json.loads(result)
        print(result)
        # result = result.json()
        LISTEN_KEY = result["listenKey"]
    except Exception as e:
        print(e)

updateKey()

POSITION_ARR = []
ASSETS_ARR =[]
def getBinancePosition():
    global REQUEST_CLIENT,ASSETS_ARR,TRADE_SYMBOL_ARR,BNB_PRICE,FUNCTION_CLIENT,POSITION_ARR,COST,COIN_BALANCE,BINANCE_API_KEY,BINANCE_API_SECRET,INSTRUMENT_ID,COIN,UPDATE_BINANCE_POSITION_DELAY_WARN_TS,UNREALIZED_PROFIT,NOW_OPEN_POSITION_COIN_AMOUNT,SYMBOL
    now = int(time.time()*1000)
    try:
        result = REQUEST_CLIENT.get_account_information()
        result = json.loads(result)
        if "code" in result:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min("getBinancePosition code:"+str(result))
        else:
            positionsArr = result["positions"]
            if len(POSITION_ARR)!=positionsArr:
                POSITION_ARR = positionsArr
            else:
                for a in range(len(POSITION_ARR)):
                    for b in range(len(positionsArr)):
                        if positionsArr[b]["symbol"]==POSITION_ARR[a]["symbol"] and positionsArr[b]["updateTime"]>POSITION_ARR[a]["updateTime"]:
                            POSITION_ARR[a]=positionsArr[b]
                            break


            assetsArr = result["assets"]
            if len(ASSETS_ARR)!=assetsArr:
                ASSETS_ARR = assetsArr
            else:
                for a in range(len(ASSETS_ARR)):
                    for b in range(len(assetsArr)):
                        if assetsArr[b]["updateTime"]>ASSETS_ARR[a]["updateTime"]:
                            ASSETS_ARR[a]=assetsArr[b]
                            break

    except Exception as e:
        print(e)

getBinancePosition()

WS = {}

def connectWs():
    global WS,LISTEN_KEY
    WS = websocket.WebSocketApp("wss://fstream.binance.com/ws/"+LISTEN_KEY,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    WS.run_forever()

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

LAST_UPDATE_KEY_TS = 0
LAST_UPDATE_POSITION_TS = 0
def on_message(ws, message):
    global LAST_UPDATE_KEY_TS,ASSETS_ARR,POSITION_ARR,LAST_UPDATE_POSITION_TS,BNB_PRICE,MACHINE_INDEX
    try:
        now = int(time.time()*1000)
        if now - LAST_UPDATE_POSITION_TS>1000:
            LAST_UPDATE_POSITION_TS = now
            _thread.start_new_thread( getBinancePosition, () )
            
            _thread.start_new_thread(updateBnbPrice,())
        print(message)
        message = json.loads(message)
        if now - LAST_UPDATE_KEY_TS>30*60*1000:
            LAST_UPDATE_KEY_TS = now
        if "e" in message and message["e"]=="listenKeyExpired":
            updateKey()
            connectWs()
        if "e" in message and message["e"]=="ACCOUNT_UPDATE":
            positionsArr = message["a"]["P"]
            for a in range(len(POSITION_ARR)):
                for b in range(len(positionsArr)):
                    if POSITION_ARR[a]["symbol"]==positionsArr[b]["s"] and message["T"]>POSITION_ARR[a]["updateTime"]:
                        POSITION_ARR[a]["entryPrice"] = positionsArr[b]["ep"]
                        POSITION_ARR[a]["positionAmt"] = positionsArr[b]["pa"]


            assetsArr = message["a"]["B"]
            for a in range(len(ASSETS_ARR)):
                for b in range(len(assetsArr)):
                    if message["T"]>ASSETS_ARR[a]["updateTime"] and ASSETS_ARR[a]["asset"]==assetsArr[b]["a"]:
                        ASSETS_ARR[a]["marginBalance"] = assetsArr[b]["wb"]

            accountBalance = 0
            for i in range(len(ASSETS_ARR)):
                if ASSETS_ARR[i]['asset'] == "USDT":
                    accountBalance = accountBalance+float(ASSETS_ARR[i]['marginBalance'])
                if ASSETS_ARR[i]['asset'] == "BUSD":
                    accountBalance = accountBalance+float(ASSETS_ARR[i]['marginBalance'])
                if ASSETS_ARR[i]['asset'] == "BNB":
                    accountBalance = accountBalance+float(ASSETS_ARR[i]['marginBalance'])*BNB_PRICE

            print("accountBalance:"+str(accountBalance))
            sendStr = "fdsoihsoaitowljd"+str(message["T"])+str(accountBalance)
            print(sendStr)
            if MACHINE_INDEX==0:
                FUNCTION_CLIENT.send_to_ws_a(sendStr)
            elif MACHINE_INDEX==1:
                FUNCTION_CLIENT.send_to_ws_b(sendStr)

            sendStr = ""
            for a in range(len(POSITION_ARR)):
                if float(POSITION_ARR[a]["entryPrice"])!=0:
                    if sendStr=="":
                        sendStr = POSITION_ARR[a]["symbol"]+"@"+POSITION_ARR[a]["entryPrice"]+"@"+POSITION_ARR[a]["positionAmt"]
                    else:
                        sendStr = sendStr+"&"+POSITION_ARR[a]["symbol"]+"@"+POSITION_ARR[a]["entryPrice"]+"@"+POSITION_ARR[a]["positionAmt"]

            sendStr = "gggoihsoaitowljd"+str(message["T"])+sendStr
            print(sendStr)
            if MACHINE_INDEX==0:
                FUNCTION_CLIENT.send_to_ws_a(sendStr)
            elif MACHINE_INDEX==1:
                FUNCTION_CLIENT.send_to_ws_b(sendStr)
    except Exception as e:
        ex = traceback.format_exc()
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    connectWs()