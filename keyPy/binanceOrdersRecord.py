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

ORDERS_TABLE_NAME = "binance_orders"


tableName = ORDERS_TABLE_NAME
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
      `avgPrice` double(30,10) NULL,
      `clientOrderId` varchar(255) NULL,
      `cumQuote` double(30,10) NULL,
      `executedQty` double(30,10) NULL,
      `orderId` bigInt(30) NULL,
      `origQty` double(30,10) NULL,
      `origType` varchar(255) NULL,
      `price` double(30,10) NULL,
      `reduceOnly` varchar(255) NULL,
      `side` varchar(255) NULL,
      `positionSide` varchar(255) NULL,
      `status` varchar(255) NULL,
      `stopPrice` double(30,10) NULL,
      `closePosition` varchar(30) NULL,
      `symbol` varchar(30) NULL,
      `timeInForce` varchar(30) NULL,
      `orderType` varchar(30) NULL,
      `updateTime` bigInt(30) NULL,
      `workingType` varchar(30) NULL,
      `priceProtect` varchar(30) NULL,
      `binanceTs` bigInt(30) NULL,
      `myTs` bigInt(30) NULL,
      PRIMARY KEY (`id`) USING BTREE
    );"""
    FUNCTION_CLIENT.mysql_commit(sql,[])


def recordTrades(symbol):
    global BINANCE_API_KEY,BINANCE_API_SECRET,ORDERS_TABLE_NAME
    now = int(time.time())

    sql = "select `binanceTs`,`orderId`,`updateTime`,`status`,`id` from "+ORDERS_TABLE_NAME+" where symbol=%s order by id desc limit 1000"
    lastBinanceTsData = FUNCTION_CLIENT.mysql_select(sql,[symbol])
    lastBinanceTs = 0
    if len(lastBinanceTsData)>0:
        lastBinanceTs = lastBinanceTsData[0][0]


    request_client = RequestClient(api_key=BINANCE_API_KEY,secret_key=BINANCE_API_SECRET)
    result = request_client.get_all_orders(symbol)
    result = json.loads(result)
    for i in range(len(result)):
        if result[i]["executedQty"]!="0" and result[i]["side"]=="SELL":
            print(result[i])
    if "code" in result:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(result))
    else:
        for i in range(len(result)):

            avgPrice = result[i]['avgPrice']
            clientOrderId = result[i]['clientOrderId']
            cumQuote = result[i]['cumQuote']
            executedQty = result[i]['executedQty']
            orderId = result[i]['orderId']

            origQty = result[i]['origQty']
            origType = result[i]['origType']
            price = result[i]['price']
            reduceOnly = result[i]['reduceOnly']
            side = result[i]['side']

            positionSide = result[i]['positionSide']
            status = result[i]['status']
            stopPrice = result[i]['stopPrice']
            closePosition = result[i]['closePosition']
            symbol = result[i]['symbol']

            timeInForce = result[i]['timeInForce']
            orderType = result[i]['type']
            updateTime = result[i]['updateTime']
            workingType = result[i]['workingType']
            priceProtect = result[i]['priceProtect']

            binanceTs = result[i]['time']
            myTs = int(time.time())


            noInsert = False
            update = False
            for b in range(len(lastBinanceTsData)):
                DBBinanceTs = lastBinanceTsData[b][0]
                DBOrderId = lastBinanceTsData[b][1]
                DBUpdateTime = lastBinanceTsData[b][2]
                DBStatus = lastBinanceTsData[b][3]
                DBID = lastBinanceTsData[b][4]
                if int(DBOrderId) == int(orderId):
                    noInsert = True
                if int(DBBinanceTs)==int(binanceTs) and int(DBOrderId) == int(orderId) and (int(DBUpdateTime) != int(updateTime) or str(DBStatus) != str(status)):
                    update = True 
            if not noInsert:
                insertSQLStr = "(%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,  %s,%s,%s,%s,%s, %s,%s)"
                sql = "INSERT INTO "+ORDERS_TABLE_NAME+" ( `avgPrice`,`clientOrderId`,`cumQuote`,`executedQty`,`orderId`,`origQty`,`origType`,`price`,`reduceOnly`,`side`,`positionSide`,`status`,`stopPrice`,`closePosition`,`symbol`,`timeInForce`,`orderType`,`updateTime`,`workingType`,`priceProtect`,`binanceTs`,`myTs`)  VALUES "+insertSQLStr+";" 
                FUNCTION_CLIENT.mysql_commit(sql,[avgPrice,clientOrderId,cumQuote,executedQty,  orderId,origQty,origType,price,reduceOnly,  side,positionSide,status,stopPrice,closePosition,  symbol,timeInForce,orderType,updateTime,workingType,  priceProtect,binanceTs,myTs])
            if update:
                sql = "update "+ORDERS_TABLE_NAME+" set `avgPrice`=%s,`clientOrderId`=%s,`cumQuote`=%s,`executedQty`=%s,`orderId`=%s,`origQty`=%s,`origType`=%s,`price`=%s,`reduceOnly`=%s,`side`=%s,`positionSide`=%s,`status`=%s,`stopPrice`=%s,`closePosition`=%s,`symbol`=%s,`timeInForce`=%s,`orderType`=%s,`updateTime`=%s,`workingType`=%s,`priceProtect`=%s,`binanceTs`=%s,`myTs`=%s where id=%s" 
                FUNCTION_CLIENT.mysql_commit(sql,[avgPrice,clientOrderId,cumQuote,executedQty,orderId,origQty,origType,price,reduceOnly,side,positionSide,status,stopPrice,closePosition,symbol,timeInForce,orderType,updateTime,workingType,priceProtect,binanceTs,myTs,DBID])

        time.sleep(3)

TRADES_ERROR_WARN_TS = 0

def updateTrade(symbol):
    global BINANCE_API_KEY,BINANCE_API_SECRET,SEND_ORDERS_CODE_ERROR_TS,TRADES_ERROR_WARN_TS,ORDERS_TABLE_NAME
    now = int(time.time())
    myTs = int(time.time())

    sql = "select `clientOrderId`,`id` from "+ORDERS_TABLE_NAME+" where status='NEW' and myTs<%s"
    data = FUNCTION_CLIENT.mysql_select(sql,[now - 3600])
    if len(data)>0:
        request_client = RequestClient(api_key=BINANCE_API_KEY,secret_key=BINANCE_API_SECRET)
        result = request_client.get_order_by_client_id(symbol,data[0][0])
        result = json.loads(result)
        if "code" in result:
            if result["code"]==-2013:
                sql = "update "+ORDERS_TABLE_NAME+" set `status`=%s,`myTs`=%s  where id=%s" 
                FUNCTION_CLIENT.mysql_commit(sql,["noExit",myTs,data[0][1]])
            else:
                FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(result))
        else:
            print(result)
            avgPrice = result['avgPrice']
            clientOrderId = result['clientOrderId']
            cumQuote = result['cumQuote']
            executedQty = result['executedQty']
            orderId = result['orderId']

            origQty = result['origQty']
            origType = result['origType']
            price = result['price']
            reduceOnly = result['reduceOnly']
            side = result['side']

            positionSide = result['positionSide']
            status = result['status']
            stopPrice = result['stopPrice']
            closePosition = result['closePosition']
            symbol = result['symbol']

            timeInForce = result['timeInForce']
            orderType = result['type']
            updateTime = result['updateTime']
            workingType = result['workingType']
            priceProtect = result['priceProtect']

            binanceTs = result['time']
            sql = "update "+ORDERS_TABLE_NAME+" set `avgPrice`=%s,`clientOrderId`=%s,`cumQuote`=%s,`executedQty`=%s,`orderId`=%s,`origQty`=%s,`origType`=%s,`price`=%s,`reduceOnly`=%s,`side`=%s,`positionSide`=%s,`status`=%s,`stopPrice`=%s,`closePosition`=%s,`symbol`=%s,`timeInForce`=%s,`orderType`=%s,`updateTime`=%s,`workingType`=%s,`priceProtect`=%s,`binanceTs`=%s,`myTs`=%s  where id=%s" 
            FUNCTION_CLIENT.mysql_commit(sql,[avgPrice,clientOrderId,cumQuote,executedQty,orderId,origQty,origType,price,reduceOnly,side,positionSide,status,stopPrice,closePosition,symbol,timeInForce,orderType,updateTime,workingType,priceProtect,binanceTs,myTs,data[0][1]])



recordTrades("MAVUSDT")
while 1:
    for i in range(len(TRADE_SYMBOL_ARR)):
        try:
            recordTrades(TRADE_SYMBOL_ARR[i]["symbol"])
            updateTrade(TRADE_SYMBOL_ARR[i]["symbol"])

        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
        time.sleep(1)
