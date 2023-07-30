#!/usr/bin/python3.10
# coding=utf-8
import time
import json
import requests
from config import *
from commonFunction import FunctionClient

#2023.07.26 发现币安出现一个bug，导致tickbook有时候返还的排序会不一定，导致了之前设计的一部分问题，目前已经解决

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="tickToWs",connectMysql =True)

privateIP = FUNCTION_CLIENT.get_private_ip()

# 此处是通过阿里云命名带有 tickToWs 后，如tickToWs_1,tickToWs_2,调用api进行搜索，如非阿里云需自行替换相关api，或者直接手动写入所有tickToWs服务器的私有地址
TICK_PRIVATE_IP_ARR = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("tickToWs")

sql = "select `symbol`,`id` from trade_symbol where `status`='yes' order by id asc" 
TRADE_SYMBOL_DATA = FUNCTION_CLIENT.mysql_select(sql,[])

TRADE_SYMBOL_ARR = []
for i in range(len(TRADE_SYMBOL_DATA)):
    TRADE_SYMBOL_ARR.append({
            "symbol":TRADE_SYMBOL_DATA[i][0],
            "id":TRADE_SYMBOL_DATA[i][1],
            "binanceIndex":-1
        })

sendStr = "bbboiyfpdufiyuyu"+str(len(TRADE_SYMBOL_ARR))
FUNCTION_CLIENT.send_to_ws_a(sendStr)

def findBinanceIndex(tickerData):
    global TRADE_SYMBOL_ARR
    for a in range(len(TRADE_SYMBOL_ARR)):
        for b in range(len(tickerData)):
            if TRADE_SYMBOL_ARR[a]["symbol"]==tickerData[b]["symbol"]:
                TRADE_SYMBOL_ARR[a]["binanceIndex"]= b
                break

url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
tickerData = requests.request("GET", url,timeout=(1,1),headers={}).json()
findBinanceIndex(tickerData)

REQUESTS_SESSION = requests.Session()

def tickToWs():
    global TRADE_SYMBOL_DATA,FUNCTION_CLIENT,REQUESTS_SESSION
    nowTs = int(time.time())
    url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    tickerData =  json.loads(REQUESTS_SESSION.get(url,timeout=(1,1)).content.decode())

    if 'code' in tickerData:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(tickerData))
    else:
        sendPriceStr = ""
        sendTs= tickerData[0]["time"]
        for a in range(len(TRADE_SYMBOL_ARR)):
            binanceIndex = TRADE_SYMBOL_ARR[a]["binanceIndex"]

            if binanceIndex==-1:
                if sendPriceStr=="":
                    sendPriceStr =  "0"
                else:
                    sendPriceStr =  sendPriceStr+"~0"
            else:

                if TRADE_SYMBOL_ARR[a]["symbol"]!=tickerData[binanceIndex]["symbol"]:
                    findBinanceIndex(tickerData)
                    binanceIndex = TRADE_SYMBOL_ARR[a]["binanceIndex"]

                if tickerData[binanceIndex]["time"]>sendTs:
                    sendTs = tickerData[binanceIndex]["time"]
                if sendPriceStr=="":
                    sendPriceStr =  tickerData[binanceIndex]["askPrice"]+"^"+tickerData[binanceIndex]["bidPrice"]+"^"+FUNCTION_CLIENT.turn_ts_to_min(tickerData[binanceIndex]["time"])
                else:
                    sendPriceStr =  sendPriceStr+"~"+tickerData[binanceIndex]["askPrice"]+"^"+tickerData[binanceIndex]["bidPrice"]+"^"+FUNCTION_CLIENT.turn_ts_to_min(tickerData[binanceIndex]["time"])


        if sendPriceStr=="":
            FUNCTION_CLIENT.send_lark_msg_limit_one_min("sendPriceStr==null:"+str(tickerData))
        else:
            tickSendStr = "sjaoihsoaitowljd"+str(sendTs)+sendPriceStr
            FUNCTION_CLIENT.send_to_ws_a(tickSendStr)


errorArr = []
for i in range(60):
    errorArr.append(0)


nowMillisecondLimitAllArr = []
for i in range(len(TICK_PRIVATE_IP_ARR)):
    nowMillisecondLimitAllArr.append([])


oneServerOneSecondRequestsTime  = 8

requestsLimitTs = 1000/oneServerOneSecondRequestsTime

for a in range(len(TICK_PRIVATE_IP_ARR)):
    for b in range(oneServerOneSecondRequestsTime):
        nowMillisecondLimitAllArr[a].append([int(a*1000/len(TICK_PRIVATE_IP_ARR)/oneServerOneSecondRequestsTime+1000/oneServerOneSecondRequestsTime*b),int((a+1)*1000/len(TICK_PRIVATE_IP_ARR)/oneServerOneSecondRequestsTime+1000/oneServerOneSecondRequestsTime*b)])

nowMillisecondLimitArrIndex = -1
for i in range(len(TICK_PRIVATE_IP_ARR)):
    if privateIP==TICK_PRIVATE_IP_ARR[i]:
        nowMillisecondLimitArrIndex = i

nowMillisecondLimitArr = nowMillisecondLimitAllArr[nowMillisecondLimitArrIndex]

FUNCTION_CLIENT.send_lark_msg_limit_one_min("start")

errorTime = 0

lastRequestTs = 0

while 1:
    FUNCTION_CLIENT.update_machine_status()
    nowTs = int(time.time()*1000)
    nowSecond = nowTs%60000
    nowMillisecond = nowTs%1000
    try:
        nowRequests = False
        for i in range(len(nowMillisecondLimitArr)):
            if nowMillisecondLimitArr[i][0]<=nowMillisecond and  nowMillisecondLimitArr[i][1]>nowMillisecond:
                nowRequests = True
        if nowRequests and nowTs - lastRequestTs>=requestsLimitTs:
            lastRequestTs = nowTs
            tickToWs()
        errorTime = 0
    except Exception as e:
        now = int(time.time())

        errorTime = errorTime+1
        if errorTime>5:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
