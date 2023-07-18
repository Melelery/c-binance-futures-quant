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

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="ordersRecord",connectMysql =True)

BINANCE_API_KEY =""

BINANCE_API_SECRET =""

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]

TRADES_TABLE_NAME = "binance_trades"


tableName = TRADES_TABLE_NAME
tableExit = False
sql ="show tables;"
tableData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tableData)):
    if tableData[a][0]==tableName:
        tableExit = True

print(tableExit)
if not tableExit:
    sql="""CREATE TABLE `"""+tableName+"""`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `buyer` int(1) NULL,
      `commission` double(30,10) NULL,
      `binanceId` bigInt(30) NULL,
      `maker` int(1) NULL,
      `orderId`  bigInt(30) NULL,
      `price` double(30,10) NULL,
      `qty` double(30,10) NULL,
      `quoteQty` double(30,10) NULL,
      `realizedPnl` double(30,10) NULL,
      `side` varchar(11) NULL,
      `positionSide` varchar(11) NULL,
      `symbol` varchar(30) NULL,
      `ts` bigInt(30) NULL,

      `myTs` int(11) NULL,
      PRIMARY KEY (`id`) USING BTREE
    );"""
    FUNCTION_CLIENT.mysql_commit(sql,[])


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
def recordTrades(symbol):
    global BINANCE_API_KEY,BINANCE_API_SECRET,TRADES_TABLE_NAME
    now = int(time.time())
    updateBnbPrice()
    sql = "select `ts`,`orderId`,`binanceId`,`id` from "+TRADES_TABLE_NAME+" where symbol=%s order by id desc limit 1000"
    tradesData = FUNCTION_CLIENT.mysql_select(sql,[symbol])
    lastBinanceTs = 0
    if len(tradesData)>0:
        lastBinanceTs = tradesData[0][0]


    request_client = RequestClient(api_key=BINANCE_API_KEY,secret_key=BINANCE_API_SECRET)
    result = request_client.get_account_trades(symbol)
    result = json.loads(result)
    print(result)
    if "code" in result:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(result))
    else:
        for i in range(len(result)):

            buyer = result[i]['buyer']
            if buyer:
                buyer = 1
            else:
                buyer = 0
            commission = result[i]['commission']
            commissionAsset = result[i]['commissionAsset']
            binanceId = result[i]['id']
            maker = result[i]['maker']
            if maker:
                maker = 1
            else:
                maker = 0

            orderId = result[i]['orderId']
            price = result[i]['price']
            qty = result[i]['qty']
            quoteQty = result[i]['quoteQty']
            realizedPnl = result[i]['realizedPnl']

            side = result[i]['side']
            positionSide = result[i]['positionSide']
            symbol = result[i]['symbol']
            binanceTs = result[i]['time']

            myTs = int(time.time())


            insert = True
            for b in range(len(tradesData)):
                DBBinanceTs = tradesData[b][0]
                DBOrderId = tradesData[b][1]
                DBBinanceId = tradesData[b][2]
                DBID = tradesData[b][3]
                if int(DBBinanceId) == int(binanceId):
                    insert = False
                    break

            if insert:
                insertSQLStr = "(%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s)"
                sql = "INSERT INTO "+TRADES_TABLE_NAME+" ( `buyer`,`commission`,`binanceId`,`maker`,`orderId`, `price`,`qty`,`quoteQty`,`realizedPnl`,`side`, `positionSide`,`symbol`,`ts`,`myTs`)  VALUES "+insertSQLStr+";" 
                FUNCTION_CLIENT.mysql_commit(sql,[buyer,commission,binanceId,maker,orderId,price,qty,quoteQty,realizedPnl,side,positionSide,symbol,binanceTs,now])


while 1:
    for i in range(len(TRADE_SYMBOL_ARR)):
        try:
            recordTrades(TRADE_SYMBOL_ARR[i]["symbol"])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
        time.sleep(1)
