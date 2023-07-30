#!/usr/bin/python3.10
# coding=utf-8
import time
import requests
import traceback
import json
import _thread
from config import *
from commonFunction import FunctionClient


FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="oneMinKlineToWs",connectMysql =True)

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
            "symbolIndex":symbolIndex
        })

sendStr = "bbboiyfpdufiyuyu"+str(len(TRADE_SYMBOL_ARR))
FUNCTION_CLIENT.send_to_ws_a(sendStr)



def takeElemZero(elem):
    return float(elem[0])

REQUESTS_SESSION = requests.Session()

def klineToWs(tradeSymbolObj):
    global TRADE_SYMBOL_DATA,FUNCTION_CLIENT,REQUESTS_SESSION
    print(tradeSymbolObj)
    url = "https://fapi.binance.com/fapi/v1/klines?symbol="+tradeSymbolObj["symbol"]+"&interval=1m&limit=45"
    klineData = json.loads(REQUESTS_SESSION.get(url,timeout=(1,1)).content.decode())
    if 'code' in klineData:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(klineData))
    else:
        try:
            url = "https://fapi.binance.com/fapi/v1/depth?symbol="+tradeSymbolObj["symbol"]+"&limit=5"
            depthData = json.loads(REQUESTS_SESSION.get(url,timeout=(1,1)).content.decode())
        except Exception as e:
            ex = traceback.format_exc()
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(ex))
        bidsPrice = 0
        asksPrice = 0
        if 'code' in depthData:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(depthData))
        else:
            bidsPrice = float(depthData["bids"][0][0])
            asksPrice = float(depthData["asks"][0][0])

        allPriceStr = ""

        twoPriceStr = ""

        for i in range(len(klineData)):
            openPrice = float(klineData[i][1])
            highPrice = float(klineData[i][2])
            lowPrice = float(klineData[i][3])
            closePrice = float(klineData[i][4])

            if i ==len(klineData)-1:

                if bidsPrice!=0 and asksPrice!=0:
                    if asksPrice>highPrice:
                        highPrice = asksPrice

                    if bidsPrice<lowPrice:
                        lowPrice = bidsPrice


                    if closePrice>openPrice:
                        closePrice = asksPrice

                    if closePrice<openPrice:
                        closePrice = bidsPrice

                if allPriceStr=="":
                    allPriceStr = str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&"+str(highPrice)+"&"+str(lowPrice)+"&"+str(closePrice)
                else:
                    allPriceStr = allPriceStr+"~"+str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&"+str(highPrice)+"&"+str(lowPrice)+"&"+str(closePrice)
            else:
                if allPriceStr=="":
                    allPriceStr = str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&0&0&"+str(closePrice)
                else:
                    allPriceStr = allPriceStr+"~"+str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&0&0&"+str(closePrice)
            if i>len(klineData)-3:
                if i ==len(klineData)-1:

                    if bidsPrice!=0 and asksPrice!=0:
                        if asksPrice>highPrice:
                            highPrice = asksPrice

                        if bidsPrice<lowPrice:
                            lowPrice = bidsPrice


                        if closePrice>openPrice:
                            closePrice = asksPrice

                        if closePrice<openPrice:
                            closePrice = bidsPrice

                    if twoPriceStr=="":
                        twoPriceStr = str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&"+str(highPrice)+"&"+str(lowPrice)+"&"+str(closePrice)
                    else:
                        twoPriceStr = twoPriceStr+"~"+str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&"+str(highPrice)+"&"+str(lowPrice)+"&"+str(closePrice)
                else:
                    if twoPriceStr=="":
                        twoPriceStr = str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&0&0&"+str(closePrice)
                    else:
                        twoPriceStr = twoPriceStr+"~"+str(FUNCTION_CLIENT.turn_ts_to_min(klineData[i][0]))+"&"+str(openPrice)+"&0&0&"+str(closePrice)

        sendStr = "sajoiyfpdufiyiry"+str(tradeSymbolObj["symbolIndex"])+twoPriceStr
        FUNCTION_CLIENT.send_to_ws_a(sendStr)

        sendStr = "sjaiyhsaoyosauio"+str(tradeSymbolObj["symbolIndex"])+allPriceStr
        FUNCTION_CLIENT.send_to_ws_a(sendStr)

    time.sleep(0.25)




VOL_IP_A = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("volAndRate_1")[0]
print("VOL_IP_A:"+VOL_IP_A)

CONDITION_AND_RATE_ARR_A = []

def getVolConditionFromMyServerA():
    global CONDITION_AND_RATE_ARR_A,VOL_IP_A
    result = {}
    try:
        url = "http://"+VOL_IP_A+"/vC.json"
        result = requests.request("GET", url,timeout=(0.5,0.5)).json()
        CONDITION_AND_RATE_ARR_A = result
    except Exception as e:
        ex = traceback.format_exc()
        print(ex)

VOL_IP_B = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("volAndRate_2")[0]

CONDITION_AND_RATE_ARR_B = []


def getVolConditionFromMyServerB():
    global CONDITION_AND_RATE_ARR_B,VOL_IP_B
    result = {}
    try:
        url = "http://"+VOL_IP_B+"/vC.json"
        result = requests.request("GET", url,timeout=(0.5,0.5)).json()
        CONDITION_AND_RATE_ARR_B = result
    except Exception as e:
        ex = traceback.format_exc()
        print(ex)

getVolConditionFromMyServerA()
getVolConditionFromMyServerB()


UPDATE_VOL_TS = 0

FUNCTION_CLIENT.send_lark_msg_limit_one_min("start")

while 1:
    try:
        now = int(time.time()*1000)
        if now - UPDATE_VOL_TS>=1000:
            _thread.start_new_thread( getVolConditionFromMyServerA, () )
            _thread.start_new_thread( getVolConditionFromMyServerB, () )
            UPDATE_VOL_TS = now
        FUNCTION_CLIENT.update_machine_status()
        dataStr = FUNCTION_CLIENT.get_from_ws_a("G")
        symbolIndex = int(dataStr)
        if now - CONDITION_AND_RATE_ARR_A[symbolIndex][4]>180000 and now - CONDITION_AND_RATE_ARR_B[symbolIndex][4]>180000:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min("CONDITION_AND_RATE_ARR DELAY")
        else:
            volConditionA = CONDITION_AND_RATE_ARR_A[symbolIndex][0]

            volConditionB = CONDITION_AND_RATE_ARR_A[symbolIndex][1]

            longsVolCondition = CONDITION_AND_RATE_ARR_A[symbolIndex][5]

            volMultiple = CONDITION_AND_RATE_ARR_A[symbolIndex][2]

            if CONDITION_AND_RATE_ARR_A[symbolIndex][4]< CONDITION_AND_RATE_ARR_B[symbolIndex][4]:
                volConditionA = CONDITION_AND_RATE_ARR_B[symbolIndex][0]

                volConditionB = CONDITION_AND_RATE_ARR_B[symbolIndex][1]

                volMultiple = CONDITION_AND_RATE_ARR_B[symbolIndex][2]

                longsVolCondition = CONDITION_AND_RATE_ARR_B[symbolIndex][5]

            if volConditionA or volConditionB or longsVolCondition:
                klineToWs(TRADE_SYMBOL_ARR[symbolIndex])

    except Exception as e:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
        print(e)
        time.sleep(0.5)
        try:
            klineToWs(TRADE_SYMBOL_ARR[i])
        except Exception as e:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
            print(e)
            time.sleep(1)

