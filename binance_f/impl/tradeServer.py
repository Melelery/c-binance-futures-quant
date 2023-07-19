#!/usr/bin/python
# coding=utf-8
import sys
from bottle import run, get, post, request,response
import json
import random
import time
import requests
import mysql.connector
import oss2
import socket
import decimal
import paramiko
import datetime
import string
from multiprocessing import Pool
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
from binance_spot.requestclient import RequestClient as SpotRequestClient
from binance_f.requestclient import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.StartInstancesRequest import StartInstancesRequest
from aliyunsdkecs.request.v20140526.StopInstancesRequest import StopInstancesRequest

SERVER_INDEX_NUM = -1

def getServerInfo():
    global SERVER_INDEX_NUM
    privateIP = ""
    try: 
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        s.connect(('8.8.8.8',80)) 
        privateIP = s.getsockname()[0] 
    finally: 
        s.close()
    nowPage =1
    emptyReq =False
    while SERVER_INDEX_NUM==-1 and not emptyReq:
        client =  AcsClient('LTAIX5RBT5EZvfNH', 'TMCklwEQ59e8IEuYAFAxdTlNfAPaTL','cn-hongkong')
        client.add_endpoint('cn-hongkong','Ecs',"ecs.cn-hongkong.aliyuncs.com")
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
            if instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]==privateIP:
                serverInfoArr = instanceInfoArr[i]["InstanceName"].split(":")
                SERVER_INDEX_NUM = int(serverInfoArr[1])
        nowPage = nowPage+1

while SERVER_INDEX_NUM==-1:
    getServerInfo()


ORDER_ID_INDEX  = SERVER_INDEX_NUM*100000

OSS_AUTH = oss2.Auth('LTAIX5RBT5EZvfNH', 'TMCklwEQ59e8IEuYAFAxdTlNfAPaTL')
OSS_BUCKET = oss2.Bucket(OSS_AUTH, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'zuibite-api')


config={
    'host':'rm-j6cixe7djpst29592qo.mysql.rds.aliyuncs.com',
    'port':3306,
    'user':'root',
    'password':'Caijiali520!',
    'database':'real',
    'charset':'utf8mb4'
}
pool = MySQLConnectionPool(pool_name = "mypool",pool_size = 30,**config)

def do_work(q,params):
    res = ()
    con = pool.get_connection()
    c = con.cursor()
    try:
        c.execute(q,params)
        res = c.fetchall()
        normal = True
    except Exception as e:
        print(e) 
        print(q) 
        print("doing error") 
        normal = False
    try:
        con.close()
    except Exception as e:
        print(q) 
        print(e) 
    return res

def do_commit(q,params):
    con = pool.get_connection()
    c = con.cursor()
    try:
        c.execute(q,params)
        con.commit()
        c.close()
        normal = True
    except Exception as e:
        print(q) 
        print(e) 
        normal = False
    try:
        con.close()
    except Exception as e:
        print(q) 
        print(e) 
        
    return normal

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

    except Exception as e:
        print(e)


def turnTsToTime(initValue):
    if str(type(initValue))=="<class 'str'>":
        timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp
    else:
        time_local = time.localtime(initValue)
        dt = time.strftime("%Y-%m-%d %H:%M:00",time_local)
        return dt

ACCOUNT_INFO_UPDATE_TS = 0
POSITION_ARR = []
ASSETS_ARR = []
def getBinanceAccountInfo(apiKey):
    global ACCOUNT_INFO_UPDATE_TS,POSITION_ARR,ASSETS_ARR
    now = int(time.time()*1000)
    if now - ACCOUNT_INFO_UPDATE_TS>300:
        positionsArr = []
        assetsArr = []
        result = {}
        bnbAmount = -1
        usdtAmount = -1
        try:
            request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
            result = request_client.get_account_information()
            result = json.loads(result)
            positionsArr = result["positions"]
            assetsArr = result["assets"]
            for i in range(len(assetsArr)):
                if assetsArr[i]['asset'] == "BNB":
                    bnbAmount = float(assetsArr[i]['marginBalance'])
                if assetsArr[i]['asset'] == "USDT":
                    usdtAmount = float(assetsArr[i]['marginBalance'])
            if bnbAmount!=-1 and bnbAmount<0.1 and usdtAmount>=100:
                buyBNB(apiIndex)

            POSITION_ARR = positionsArr
            ASSETS_ARR = assetsArr
        except Exception as e:
            print(e)
        ACCOUNT_INFO_UPDATE_TS = now
    return [POSITION_ARR,ASSETS_ARR]

@post('/ping', methods='POST')
def ping():
    global PRIVATE_IP_OBJ,API_OBJ
    apiKey = str(request.forms.get('apiKey'))
    updateAPIObj(apiKey)
    instrumentID = str(request.forms.get('instrumentID'))

    now = int(time.time())

    binanceInfoArr = getBinanceAccountInfo(apiIndex)

    print(int(time.time())-now)
    resp = json.dumps({'s':'ok','i':instrumentIDArr,'p':binanceInfoArr[0],'t':binanceInfoArr[1],'n':now})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/get_symbol_index', methods='POST')
def getSymbolIndex():
    sql = "select `symbol`,`id`,`coin` from trade_symbol where `status`='yes' order by id asc" 
    tradeSymbolData = do_work(sql,[])

    tradeSymbolArr = []
    for i in range(len(tradeSymbolData)):
        symbolIndex = i
        tradeSymbolArr.append({
                "symbol":tradeSymbolData[i][0],
                "coin":tradeSymbolData[i][2],
                "symbolIndex":symbolIndex,
                "weight":0
            })


    resp = json.dumps({'s':'ok','d':tradeSymbolArr})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/record_player', methods='POST')
def record_player():
    page = str(request.forms.get('page'))
    ip = request.environ.get('REMOTE_ADDR')
    sql = "INSERT INTO 0_player_record ( ip,`time`,`page`)  VALUES ( %s, %s,%s );" 
    do_commit(sql,[ip,turnTsToTime(int(time.time())),page])
    resp = json.dumps({'s':'ok'})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp



@post('/register', methods='POST')
def register():
    account = str(request.forms.get('account'))
    password = str(request.forms.get('password'))
    newHotKeyConfigObj = str(request.forms.get('newHotKeyConfigObj'))
    ip = request.environ.get('REMOTE_ADDR')
    name = str(request.forms.get('name'))
    if len(account)<4 or len(account)>20:
        resp = json.dumps({'s':'accountLengthError'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    if len(password)<4 or len(password)>20:
        resp = json.dumps({'s':'passwordLengthError'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    if len(name)<1 or len(name)>20:
        resp = json.dumps({'s':'nameLengthError'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp

    sql = "select `id` from user where `account`=%s" 
    userData = do_work(sql,[account])

    if len(userData)>0:
        resp = json.dumps({'s':'repeatRegister'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp

    accessToken = ''.join(random.sample(string.ascii_letters + string.digits, 30))
    sql = "INSERT INTO user ( `registerIP`,account,`password`,`name`,`registerTime`,`binanceApiArr`,`hotKeyConfigObj`,`stateConfigObj`,`serverInfoObj`,`accessToken`)  VALUES ( %s,%s,%s,%s, %s,%s ,%s,%s,%s,%s );" 
    do_commit(sql,[ip,account,password,name,turnTsToTime(int(time.time())),json.dumps([]),json.dumps(json.loads(newHotKeyConfigObj)),json.dumps({}),json.dumps({}),accessToken])
    resp = json.dumps({'s':'ok'})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/login', methods='POST')
def login():
    account = str(request.forms.get('account'))
    password = str(request.forms.get('password'))

    sql = "select `password`,`usdtAssets`,`binanceApiArr`,`hotKeyConfigObj`,`stateConfigObj`,`serverInfoObj`,`name`,`accessToken` from user where `account`=%s " 
    userData = do_work(sql,[account])
    if len(userData)==0:
        resp = json.dumps({'s':'noRegister'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    elif userData[0][0]!=password:
        resp = json.dumps({'s':'passwordError'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    else:
        binanceApiArr = json.loads(userData[0][2])
        for i in range(len(binanceApiArr)):
            binanceApiArr[i]["apiSecret"]=""
        resp = json.dumps({'s':'ok','account':account,'password':userData[0][0],'usdtAssets':userData[0][1],'binanceApiArr':json.loads(userData[0][2]),"hotKeyConfigObj":json.loads(userData[0][3]),"stateConfigObj":json.loads(userData[0][4]),"serverInfoObj":json.loads(userData[0][5]),"name":userData[0][6],"accessToken":userData[0][7]})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp


@post('/add_api', methods='POST')
def add_api():
    accessToken = str(request.forms.get('accessToken'))
    apiKey = str(request.forms.get('apiKey'))
    apiSecret = str(request.forms.get('apiSecret'))
    apiDescribe = str(request.forms.get('apiDescribe'))

    request_client = RequestClient(api_key=apiKey,secret_key=apiSecret)
    result = request_client.get_position()
    result = json.loads(result)
    print(type(result))
    # {'code': -2014, 'msg': 'API-key format invalid.'}
    if 'code' in result and result['code']==-2014:
        resp = json.dumps({'s':'error'})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    else:

        sql = "select `binanceApiArr` from user where `accessToken`=%s " 
        userData = do_work(sql,[accessToken])
        binanceApiArr = json.loads(userData[0][0])
        binanceApiArr.append({"apiKey":apiKey,"apiSecret":apiSecret,"apiDescribe":apiDescribe})
        sql = "update user set `binanceApiArr`=%s where `accessToken`=%s " 
        do_commit(sql,[json.dumps(binanceApiArr),accessToken])
        resp = json.dumps({'s':'ok',"binanceApiArr":binanceApiArr})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp



@post('/delete_api', methods='POST')
def delete_api():
    accessToken = str(request.forms.get('accessToken'))
    apiKey = str(request.forms.get('apiKey'))

    sql = "select `binanceApiArr` from user where `accessToken`=%s " 
    userData = do_work(sql,[accessToken])
    binanceApiArr = json.loads(userData[0][0])

    deleteIndex = -1
    for i in range(len(binanceApiArr)):
        if binanceApiArr[i]["apiKey"]==apiKey:
            deleteIndex = i
    if deleteIndex!=-1:
        del binanceApiArr[deleteIndex]
    sql = "update user set `binanceApiArr`=%s where `accessToken`=%s " 
    do_commit(sql,[json.dumps(binanceApiArr),accessToken])
    resp = json.dumps({'s':'ok',"binanceApiArr":binanceApiArr})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp



@post('/modify_hot_key', methods='POST')
def modify_hot_key():
    accessToken = str(request.forms.get('accessToken'))
    newHotKeyConfigObj = str(request.forms.get('newHotKeyConfigObj'))
    sql = "update user set `hotKeyConfigObj`=%s where `accessToken`=%s " 
    do_commit(sql,[json.dumps(json.loads(newHotKeyConfigObj)),accessToken])
    resp = json.dumps({'s':'ok',"newHotKeyConfigObj":newHotKeyConfigObj})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/get_state_config', methods='POST')
def get_state_config():
    accessToken = str(request.forms.get('accessToken'))
    apiKey = str(request.forms.get('apiKey'))

    sql = "select `stateConfigObj` from user where `accessToken`=%s " 
    userData = do_work(sql,[accessToken])
    stateConfigObj = json.loads(userData[0][0])
    resp = json.dumps({'s':'ok',"stateConfigObj":stateConfigObj})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/modify_state_config', methods='POST')
def modify_state_config():
    accessToken = str(request.forms.get('accessToken'))
    stateConfigOBj = str(request.forms.get('stateConfigOBj'))
    sql = "update user set `stateConfigObj`=%s where `accessToken`=%s " 
    do_commit(sql,[json.dumps(json.loads(stateConfigOBj)),accessToken])
    resp = json.dumps({'s':'ok'})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

DEPTH_UPDATE_TS = 0
LAST_BINANCE_RESPONSE_OBJ = {}
@post('/get_depth', methods='POST')
def get_depth():
    global PRICE_DECIMAL_AMOUNT_OBJ,AMOUNT_DECIMAL_AMOUNT_OBJ,DEPTH_UPDATE_TS,LAST_BINANCE_RESPONSE
    symbol = str(request.forms.get('symbol'))
    now = int(time.time()*1000)
    if now - DEPTH_UPDATE_TS>100:
        DEPTH_UPDATE_TS = now
        url = "https://fapi.binance.com/fapi/v1/depth?symbol="+symbol+"&limit=50"
        binanceResponse = requests.request("GET", url,timeout=(0.5,0.5)).json()
        LAST_BINANCE_RESPONSE_OBJ = binanceResponse
    resp = json.dumps({'s':'ok','r':LAST_BINANCE_RESPONSE_OBJ,"i":symbol,"p":PRICE_DECIMAL_AMOUNT_OBJ[symbol],"a":AMOUNT_DECIMAL_AMOUNT_OBJ[symbol]})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

API_OBJ = {}
def updateAPIObj(apiKey):
    global API_OBJ
    if apiKey in API_OBJ:
        return
    else:
        sql = "select `binanceApiArr` from user" 
        userData = do_work(sql,[])
        for a in range(len(userData)):
            binanceApiArr = json.loads(userData[a][0])
            for b in range(len(binanceApiArr)):
                if apiKey==binanceApiArr[b]["apiKey"]:
                    API_OBJ[binanceApiArr[b]["apiKey"]]=binanceApiArr[b]["apiSecret"]
                    break

def cancelBinanceOrder(symbol,apiKey):
    global API_OBJ
    try:
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.cancel_all_orders(symbol=symbol)
        result = json.loads(result)
    except Exception as e:
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.cancel_all_orders(symbol=symbol)
        result = json.loads(result)
        print(e)

@post('/cancel_orders', methods='POST')
def cancel_orders():
    global API_OBJ
    apiKey = str(request.forms.get('apiKey'))
    updateAPIObj(apiKey)
    symbol = str(request.forms.get('symbol'))
    cancelBinanceOrder(symbol,apiKey)
    resp = json.dumps({'s':'ok'})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

@post('/cancel_order', methods='POST')
def cancel_order():
    global API_OBJ
    apiKey = str(request.forms.get('apiKey'))
    updateAPIObj(apiKey)
    symbol = str(request.forms.get('symbol'))
    clientOrderId = str(request.forms.get('clientOrderId'))
    print(symbol)
    print(orderID)
    print(apiKey)
    request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
    result = request_client.cancel_order(symbol=symbol,orderId=clientOrderId)
    resp = json.dumps({'s':'ok'})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp

ALL_OPEN_ORDERS_ARR_UPDATE_TS = 0
ALL_OPEN_ORDERS_ARR = []
@post('/get_all_open_orders', methods='POST')
def get_all_open_orders():
    global API_OBJ,ALL_OPEN_ORDERS_ARR,ALL_OPEN_ORDERS_ARR_UPDATE_TS
    apiKey = str(request.forms.get('apiKey'))
    updateAPIObj(apiKey)
    now  = int(time.time())
    result = {}
    if now-ALL_OPEN_ORDERS_ARR_UPDATE_TS>1:
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.get_all_open_orders()
        result = json.loads(result)
        ALL_OPEN_ORDERS_ARR = result
        ALL_OPEN_ORDERS_ARR_UPDATE_TS = now
    resp = json.dumps({'s':'ok','r':ALL_OPEN_ORDERS_ARR})
    response.set_header('Access-Control-Allow-Origin', '*')
    return resp


@post('/trade', methods='POST')
def trade():
    global API_OBJ,PRICE_DECIMAL_OBJ,AMOUNT_DECIMAL_OBJ,RECENT_ORDERS_OBJ,ORDER_ID_INDEX

    apiKey = str(request.forms.get('apiKey'))
    symbol = str(request.forms.get('symbol'))
    money = float(request.forms.get('money'))
    tradeType = str(request.forms.get('tradeType'))
    price = float(request.forms.get('price'))
    now = int(time.time())
    updateAPIObj(apiKey)

    if tradeType=="marketOpenLongs":
        coinQuantity =  float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (money/price )))
        # thisPrice =  float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (price*1.002)))
        ORDER_ID_INDEX = ORDER_ID_INDEX+1
        newClientOrderId = "takerOpenLongs_s"+str(ORDER_ID_INDEX)
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.BUY, ordertype=OrderType.MARKET, positionSide="BOTH", price="0")
        result = json.loads(result)
        resp = json.dumps({'s':'ok','result':result,'money':money,'symbol':symbol})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    elif tradeType=="marketOpenShorts":
        coinQuantity =  float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (money/price )))
        # thisPrice =  float(decimal.Decimal(PRICE_DECIMAL_OBJ[symbol] % (price*0.998)))
        ORDER_ID_INDEX = ORDER_ID_INDEX+1
        newClientOrderId = "takerOpenShorts_s"+str(ORDER_ID_INDEX)
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.post_market_order(newClientOrderId=newClientOrderId,reduceOnly=False,symbol=symbol, quantity=coinQuantity,side=OrderSide.SELL, ordertype=OrderType.MARKET, positionSide="BOTH", price="0")
        result = json.loads(result)
        resp = json.dumps({'s':'ok','result':result,'money':money,'symbol':symbol})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    elif tradeType=="longsForceCloseBySelectCoin":
        marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]

        newClientOrderId = "longsForceClose_s"+str(ORDER_ID_INDEX)
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.post_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=thisPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        coinQuantity =  float(decimal.Decimal(AMOUNT_DECIMAL_OBJ[symbol] % (money/price )))
        resp = json.dumps({'s':'ok','result':result,'coinQuantity':coinQuantity,'marketMaxSize':marketMaxSize,'symbol':symbol})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp
    elif tradeType=="shortsForceCloseBySelectCoin":
        marketMaxSize = MARKET_MAX_SIZE_OBJ[symbol]

        newClientOrderId = "longsForceClose_s"+str(ORDER_ID_INDEX)
        request_client = RequestClient(api_key=apiKey,secret_key=API_OBJ[apiKey])
        result = request_client.post_order(newClientOrderId=newClientOrderId,reduceOnly=True,symbol=symbol, quantity=marketMaxSize,side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=thisPrice, positionSide="BOTH", timeInForce=TimeInForce.GTC)
        result = json.loads(result)
        resp = json.dumps({'s':'ok','result':result,'coinQuantity':coinQuantity,'marketMaxSize':marketMaxSize,'symbol':symbol})
        response.set_header('Access-Control-Allow-Origin', '*')
        return resp

def main():
    run(server='paste', host='0.0.0.0', port=8888)

if __name__ == "__main__":
    sys.exit(main())
