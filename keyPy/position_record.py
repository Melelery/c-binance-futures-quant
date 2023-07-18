#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果
import urllib
import decimal
import time
import mysql.connector
import requests
import uuid
import oss2
import json
import socket
import copy
import hmac
import hashlib
import base64
from binance_f.impl.utils.apisignature import create_signature
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from datetime import datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from websocket import create_connection
from mysql.connector.pooling import MySQLConnectionPool
from config import *
from commonFunction import FunctionClient
PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

TRADE_SYMBOL_ARR =  []

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()
TRADE_SYMBOL_ARR = response["d"]


print(TRADE_SYMBOL_ARR)

def turnTsToTime(initValue):
    if str(type(initValue))=="<class 'str'>":
        timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp
    else:
        if (initValue > 100000000000):
            initValue = initValue / 1000
        time_local = time.localtime(initValue)
        dt = time.strftime("%Y-%m-%d %H:%M:00",time_local)
        return dt


def sendMsg(content):
    try:
        header = {"Content-Type": "application/json"}

        body = {
            "app_id":"cli_9f1556ad73f2500c",
            "app_secret":"CrIQU6XtzEeFWT44NfFcgfooZt237Efy"
        }
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

        response = requests.request("POST", url, timeout=3, headers=header, data=json.dumps(body)).json()
        print(response)

        TEAM_ID = 'oc_d2fc6f3c0ff4d45811dfc774daec528c'
        url = "https://open.feishu.cn/open-apis/message/v4/send/"
        Authorization = "Bearer "+response['tenant_access_token']
        header = {"Authorization": Authorization,"Content-Type":"application/json"}

        sendText = content+"<at user_id='all'>test</at>"
        print(sendText)
        body = {
            "chat_id":TEAM_ID,
            "msg_type":"text",
           "content":{
                "text":sendText
            }
        }
        data = bytes(json.dumps(body), encoding='utf8')
        response = requests.request("POST", url, timeout=3, headers=header, data=data).json()
        print(response)
    except Exception as e:
        print(e)

config={
    'host':'rm-6wef0360yz959bvmx.mysql.japan.rds.aliyuncs.com',
    'port':3306,
    'user':'maker',
    'password':'Caijiali520!',
    'database':'real',
    'charset':'utf8mb4'
}
con=mysql.connector.connect(**config)


def do_work(sql,params):
    global con,config
    res = ()
    normal = ""
    try: 
       con.ping() 
    except Exception as e:      
       con=mysql.connector.connect(**config)
    while normal=="":
        try:
            cursor=con.cursor()
            cursor.execute(sql,params)
            res = cursor.fetchall()
            normal="go"
            cursor.close()
        except Exception as e:
            sendMsg("commission mysql ex,"+str(e))
            print("mysql error")
            print(sql)
            try: 
               con.ping() 
            except Exception as e:      
               con=mysql.connector.connect(**config)
            time.sleep(3)
    return res

def do_commit(sql,params):
    global con,config
    normal = ""
    try: 
       con.ping() 
    except Exception as e:      
       con=mysql.connector.connect(**config)
    while normal=="":
        try:
            cursor=con.cursor()
            cursor.execute(sql,params)
            con.commit()
            normal = "go"
            cursor.close()
        except Exception as e:
            sendMsg("commission mysql ex,"+str(e))
            print("mysql error")
            print(sql)
            try: 
               con.ping() 
            except Exception as e:      
               con=mysql.connector.connect(**config)
            time.sleep(3)

privateIP = ""
try: 
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    s.connect(('8.8.8.8',80)) 
    privateIP = s.getsockname()[0] 
finally: 
    s.close()

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
    sendMsg("mainConsole updateSymbolInfo")
    updateSymbolInfo()
    time.sleep(1)


LAST_SHORT_LOSS_LOCK_TS = 0


BINANCE_API_KEY_ARR=["WqGYwxXHwYgTmBK9jpDeuFvpGTPpclQSGKAez1aMEAUt7ME8R9qsIktdtxrKTc6Q"]
BINANCE_API_SECRET_ARR = ["LLLhzRFM6hFoaYdOZl3pSTsxKGuMKdIFto66mf9y83j8xPx7wvGe4f6lycqIsFNC"]
ACCOUNT_SYMBOL = ["take"]

POSITION_SERVER_IP_ARR = []

for i in range(len(ACCOUNT_SYMBOL)):
    POSITION_SERVER_IP_ARR.append("")

def getServerInfo():
    global POSITION_SERVER_IP_ARR

    nowPage =1
    emptyReq =False
    while not emptyReq:
        client =  AcsClient('LTAI5tDkjyCAYHGHAadbVxtv', 'onGH2W2avi114HaCmeQjffy9i6IJTr','ap-northeast-1')
        client.add_endpoint('ap-northeast-1','Ecs',"ecs.ap-northeast-1.aliyuncs.com")
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
        for i in range(len(instanceInfoArr)):
            for symbolNumber in range(len(ACCOUNT_SYMBOL)):
                if instanceInfoArr[i]["InstanceName"]=="getBinancePosition_"+ str(ACCOUNT_SYMBOL[symbolNumber]):
                    POSITION_SERVER_IP_ARR[symbolNumber] =  instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]
        nowPage = nowPage+1

getServerInfo()

print(POSITION_SERVER_IP_ARR)
# for i in range(len(INCOME_TABLE_NAME_ARR)):
#     tableName = INCOME_TABLE_NAME_ARR[i]
#     tableExit = False
#     sql ="show tables;"
#     tableData = do_work(sql,[])
#     for a in range(len(tableData)):
#         if tableData[a][0]==tableName:
#             tableExit = True

#     print(tableExit)
#     if not tableExit:
#         sql="""CREATE TABLE `"""+tableName+"""`  (
#           `id` int(11) NOT NULL AUTO_INCREMENT,
#           `incomeType` varchar(255) NULL,
#           `income` double(30,10) NULL,
#           `bnbPrice` double(30,10) NULL,
#           `asset` varchar(255) NULL,
#           `info` varchar(255) NULL,
#           `trade_id` varchar(255) NULL,
#           `binance_ts` bigint(18) NULL,
#           `my_ts` int(11) NULL,
#           `symbol` varchar(255) NULL,
#           `instrument_id` varchar(255) NULL,
#           `coin` varchar(255) NULL,
#           PRIMARY KEY (`id`) USING BTREE
#         );"""
#         do_commit(sql,[])

def getBNBPrice():
    nowPrice = 0
    tryTime = 0
    while nowPrice==0:
        try:
            url = "https://api.binance.com/api/v1/depth?symbol=BNBUSDT&limit=5"
            response = requests.request("GET", url,timeout=(3,7)).json()
            nowPrice = (float(response['asks'][0][0])+float(response['bids'][0][0])) /2
        except Exception as e:
            tryTime = tryTime+1
            time.sleep(1)
            if tryTime>3:
                sendMsg("commission 读取bnb价格出错")
            print(e)
    return nowPrice


POSITION_ARR = []
ASSETS_ARR = []
ACCOUNT_BALANCE_VALUE = 0
EIGHT_HOURS_PROFIT = 0

def getBinancePosition(index):
    global ACCOUNT_BALANCE_VALUE,POSITION_ARR,BINANCE_API_KEY_ARR,BINANCE_API_SECRET_ARR,ASSETS_ARR

    errorTime = 0
    while errorTime<3:
        result = {}
        try:
            REQUEST_CLIENT = RequestClient(api_key=BINANCE_API_KEY_ARR[index],secret_key=BINANCE_API_SECRET_ARR[index])
            result = REQUEST_CLIENT.get_account_information()
            result = json.loads(result)
            POSITION_ARR = result["positions"]
            ASSETS_ARR = result["assets"]

            ACCOUNT_BALANCE_VALUE = 0
            for i in range(len(ASSETS_ARR)):
                if ASSETS_ARR[i]['asset'] == "USDT":
                    ACCOUNT_BALANCE_VALUE = ACCOUNT_BALANCE_VALUE+float(ASSETS_ARR[i]['marginBalance'])
                if ASSETS_ARR[i]['asset'] == "BUSD":
                    ACCOUNT_BALANCE_VALUE = ACCOUNT_BALANCE_VALUE+float(ASSETS_ARR[i]['marginBalance'])

            errorTime = 100
        except Exception as e:
            errorTime = errorTime +1
            print(e)
            print("getBinancePosition 1")
            print(result)
            if errorTime>=3:
                sendMsg("【错误】, updateMyPosition Exception,"+str(e))
            time.sleep(0.25)
    if errorTime==100:
        return True
    else:
        return False


def getBinancePositionFromMyServer(index):
    global ACCOUNT_BALANCE_VALUE,POSITION_ARR,BINANCE_API_KEY_ARR,POSITION_SERVER_IP_ARR,EIGHT_HOURS_PROFIT
    errorTime = 0
    while errorTime<100:
        result = {}
        try:
            thisIP = POSITION_SERVER_IP_ARR[index]
            url = "http://172.24.206.249/"+BINANCE_API_KEY_ARR[index][0:10]+".json"
            result = requests.request("GET", url,timeout=(0.5,0.5)).json()
            POSITION_ARR = result["positionArr"]
            ACCOUNT_BALANCE_VALUE = result["balance"]
            EIGHT_HOURS_PROFIT = result["eightHoursProfit"]
            errorTime = 100
        except Exception as e:
            errorTime = errorTime +1
            print(e)
            print("getBinancePosition 1")
            print(result)
            if errorTime>=2:
                sendMsg("【错误】，updateMyPosition Exception,"+str(e))
                getBinancePosition(index)
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
        unrealizedProfit = float(POSITION_ARR[positionIndex]["unrealizedProfit"])
        maintMargin = float(POSITION_ARR[positionIndex]["maintMargin"])
        if thisSymbol == symbol:
            return [symbolPositionAmt,symbolCost,unrealizedProfit,maintMargin]
    return [0,0,0,0]


def getFutureDepthBySymbol(symbol,limit):
    response = {}
    errorTime = 0
    while errorTime<100:
        try:
            url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit="+str(limit)
            response = requests.request("GET", url,timeout=(0.5,0.5)).json()
            errorTime = 100
        except Exception as e:
            print(e)
            errorTime = errorTime+1
            time.sleep(errorTime*0.5)
    return response


UPDATE_TS = 0
def record_position():
    global BINANCE_API_KEY_ARR,BINANCE_API_SECRET_ARR,TABLE_NAME_ARR,UPDATE_TS,ACCOUNT_BALANCE_VALUE,EIGHT_HOURS_PROFIT,ACCOUNT_SYMBOL,SYMBOL_ARR,PRICE_DECIMAL_OBJ

    now = int(time.time())
    allPositionAmt = 0
    allUnrealizedProfit = 0
    allPositionValue = 0
    allBalance = 0

    if now - UPDATE_TS>60:
        for index in range(len(ACCOUNT_SYMBOL)):
            positionTableName = "position_record_"+ACCOUNT_SYMBOL[index]
            getBinancePositionFromMyServer(index)
            for tradeSymbolIndex in range(len(TRADE_SYMBOL_ARR)):
                symbol = TRADE_SYMBOL_ARR[tradeSymbolIndex]["symbol"]
                symbolPositionInfoArr = getPositionInfoArrBySymbol(symbol)
                symbolPositionAmt = symbolPositionInfoArr[0]
                symbolCost = symbolPositionInfoArr[1]
                unrealizedProfit = symbolPositionInfoArr[2]
                maintMargin = symbolPositionInfoArr[3]
                symbolCost =  decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (symbolCost))

                allUnrealizedProfit = allUnrealizedProfit+symbolPositionInfoArr[2]
                allPositionAmt = allPositionAmt+symbolPositionInfoArr[0]
                allBalance = allBalance+ACCOUNT_BALANCE_VALUE
                UPDATE_TS = now
                depthObj = getFutureDepthBySymbol(symbol,5)
                midPrice = (float(depthObj["bids"][0][0])+float(depthObj["asks"][0][0])) /2
                allPositionValue = allPositionValue+abs(symbolPositionAmt*midPrice)
                # insertSQLStr = "('"+str(symbol)+"','"+str(symbolCost)+"','"+str(unrealizedProfit)+"','"+str(maintMargin)+"','"+str(symbolPositionAmt)+"','"+str(now)+"','"+str(turnTsToTime(now))+"','"+str(midPrice)+"','"+str(abs(symbolPositionAmt*midPrice))+"','"+str(ACCOUNT_BALANCE_VALUE)+"','"+str(EIGHT_HOURS_PROFIT)+"')"
                # sql = "INSERT INTO "+positionTableName+" ( `symbol`,`entryPrice`,`unrealizedProfit`,`maintMargin`, `positionAmt`,`ts`,`time`,`price`,`positionValue`,`balance`,`eightHoursProfit`)  VALUES "+insertSQLStr+";" 
                # do_commit(sql,[])

        insertSQLStr = "('all','"+str(allUnrealizedProfit)+"','"+str(allPositionAmt)+"','"+str(now)+"','"+str(turnTsToTime(now))+"','"+str(allPositionValue)+"','"+str(ACCOUNT_BALANCE_VALUE)+"')"
        sql = "INSERT INTO position_record_take ( `symbol`,`unrealizedProfit`, `positionAmt`,`ts`,`time`,`positionValue`,`balance`)  VALUES "+insertSQLStr+";" 
        do_commit(sql,[])

UPDATE_PROFIT_AND_COMMISSION_TS  = 0
def updateProfitAndCommission():
    global UPDATE_PROFIT_AND_COMMISSION_TS,ACCOUNT_SYMBOL
    now = int(time.time())
    if now - UPDATE_PROFIT_AND_COMMISSION_TS>60:
        UPDATE_PROFIT_AND_COMMISSION_TS = now
        for index in range(len(ACCOUNT_SYMBOL)):
            positionTableName = "position_record_"+ACCOUNT_SYMBOL[index]
            incomeTableName = "income_history_"+ACCOUNT_SYMBOL[index]
            sql = "select ts,id from "+positionTableName+"  where ts<%s and updateProfitAndCommission=0 order by id desc"
            positionRecordData = do_work(sql,[now-60*30])
            if len(positionRecordData)>1:
                for i in range(len(positionRecordData)-1):
                    thisID = positionRecordData[i][1]
                    sql = "SELECT `ts`,`id` from "+positionTableName+"  where `id` = (SELECT max(`id`) FROM "+positionTableName+" where `id`<%s)"
                    lastPositionRecordData = do_work(sql,[thisID])
                    if len(lastPositionRecordData)>0:
                        endTs = positionRecordData[i][0]
                        beginTs = lastPositionRecordData[0][0]
                        allProfit = 0
                        allCommission = 0
                        allMakerCommission = 0
                        sql = "select income,incomeType,asset,bnbPrice from "+incomeTableName+"  where binance_ts>%s and binance_ts<=%s  order by id asc"
                        incomeData = do_work(sql,[beginTs*1000,endTs*1000])
                        for b in range(len(incomeData)):
                            if incomeData[b][1]=="COMMISSION":
                                if incomeData[b][2]=="BNB":
                                    allCommission = allCommission+incomeData[b][0]*incomeData[b][3]
                                else:
                                    allCommission = allCommission+incomeData[b][0]
                                if incomeData[b][0]>0:
                                    if incomeData[b][2]=="BNB":
                                        allMakerCommission = allMakerCommission+incomeData[b][0]*incomeData[b][3]
                                    else:
                                        allMakerCommission = allMakerCommission+incomeData[b][0]
                            if incomeData[b][1]=="REALIZED_PNL":
                                allProfit = allProfit+incomeData[b][0]
                        sql = "update "+positionTableName+" set profit=%s,commission=%s,makerCommission=%s,updateProfitAndCommission=1 where id =%s"
                        do_commit(sql,[allProfit,allCommission,allMakerCommission,thisID])

ERROR_TIME = 0
while 1:
    try:
        record_position()
        # updateProfitAndCommission()
        ERROR_TIME = 0
    except Exception as e:
        ERROR_TIME = ERROR_TIME+1
        if ERROR_TIME>3:
            sendMsg("【position record异常】，"+str(e)+privateIP)
        time.sleep(1)
        print(e)
    time.sleep(3)
