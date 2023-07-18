#!/usr/bin/python3.10
# coding=utf-8
import time
import requests
import json
from config import *
from commonFunction import FunctionClient

PUBLIC_SERVER_IP = "http://"+WEB_ADDRESS+":8888/"

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="volCondition",connectMysql =True)

privateIP = FUNCTION_CLIENT.get_private_ip()

response = requests.request("POST", PUBLIC_SERVER_IP+"get_symbol_index", timeout=3).json()

TRADE_SYMBOL_ARR = response["d"]


INFO_ARR = []

for i in range(len(TRADE_SYMBOL_ARR)):
    INFO_ARR.append([0,0,0,0,0,0]) #conditionA,conditionB,multiple,standard rate,update ts,longs condition

def takeElemZero(elem):
    return float(elem[0])

STAND_LOW_RATE = 0.5
def getBTCRange():
    global STAND_LOW_RATE,FUNCTION_CLIENT
    url = "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m&limit=499"
    klineData = requests.request("GET", url,timeout=(3,3),headers={}).json()
    threeDaysHighPrice = 0
    threeDaysLowPrice = 99999999999
    oneDayHighPrice = 0
    oneDayLowPrice = 99999999999
    for i in range(96):
        if oneDayHighPrice<float(klineData[len(klineData)-1-i-1][2]):
            oneDayHighPrice = float(klineData[len(klineData)-1-i-1][2])
        if oneDayLowPrice>float(klineData[len(klineData)-1-i-1][3]):
            oneDayLowPrice = float(klineData[len(klineData)-1-i-1][3])
    for i in range(96*3):
        if threeDaysHighPrice<float(klineData[len(klineData)-1-i-1][2]):
            threeDaysHighPrice = float(klineData[len(klineData)-1-i-1][2])
        if threeDaysLowPrice>float(klineData[len(klineData)-1-i-1][3]):
            threeDaysLowPrice = float(klineData[len(klineData)-1-i-1][3])
    btcOneDayWave = int(FUNCTION_CLIENT.get_percent_num(oneDayHighPrice-oneDayLowPrice,oneDayLowPrice))
    btcThreeDaysWave = int(FUNCTION_CLIENT.get_percent_num(threeDaysHighPrice-threeDaysLowPrice,threeDaysLowPrice))


    url = "https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=15m&limit=499"
    klineData = requests.request("GET", url,timeout=(3,3),headers={}).json()
    threeDaysHighPrice = 0
    threeDaysLowPrice = 99999999999
    oneDayHighPrice = 0
    oneDayLowPrice = 99999999999
    for i in range(96):
        if oneDayHighPrice<float(klineData[len(klineData)-1-i-1][2]):
            oneDayHighPrice = float(klineData[len(klineData)-1-i-1][2])
        if oneDayLowPrice>float(klineData[len(klineData)-1-i-1][3]):
            oneDayLowPrice = float(klineData[len(klineData)-1-i-1][3])
    for i in range(96*3):
        if threeDaysHighPrice<float(klineData[len(klineData)-1-i-1][2]):
            threeDaysHighPrice = float(klineData[len(klineData)-1-i-1][2])
        if threeDaysLowPrice>float(klineData[len(klineData)-1-i-1][3]):
            threeDaysLowPrice = float(klineData[len(klineData)-1-i-1][3])
    ethOneDayWave = int(FUNCTION_CLIENT.get_percent_num(oneDayHighPrice-oneDayLowPrice,oneDayLowPrice))
    ethThreeDaysWave = int(FUNCTION_CLIENT.get_percent_num(threeDaysHighPrice-threeDaysLowPrice,threeDaysLowPrice))

    btcStandardWave = btcOneDayWave
    if btcThreeDaysWave/2>btcOneDayWave:
        btcStandardWave = btcThreeDaysWave/2


    ethStandardWave = ethOneDayWave
    if ethThreeDaysWave/2>ethOneDayWave:
        ethStandardWave = ethThreeDaysWave/2

    standardWave = ethStandardWave
    if btcStandardWave>standardWave:
        standardWave = btcStandardWave
    STAND_LOW_RATE = standardWave/8.5
    if STAND_LOW_RATE<0.7:
        STAND_LOW_RATE = 0.7

def updateVol(symbol,index):
    global CONDITION_A_OBJ,CONDITION_B_OBJ,MULTIPLE_OBJ,INFO_ARR,STAND_LOW_RATE
    try:
        now = int(time.time()*1000)
        url = "https://fapi.binance.com/fapi/v1/klines?symbol="+symbol+"&interval=15m&limit=499"
        klineData = requests.request("GET", url,timeout=(3,3),headers={}).json()
        if 'code' in klineData:
            FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(klineData))
        else:
            klineData.sort(key=takeElemZero,reverse=False)
            threeDaysAllVol = 0
            oneDayAllVol = 0
            oneDayHighPrice = 0 
            oneDayLowPrice = 999999999
            for i in range(288):
                threeDaysAllVol = threeDaysAllVol+float(klineData[len(klineData)-1-i-1][7])
                if i<96:
                    oneDayAllVol = oneDayAllVol+float(klineData[len(klineData)-1-i-1][7])
                    if oneDayHighPrice<float(klineData[len(klineData)-1-i-1][2]):
                        oneDayHighPrice = float(klineData[len(klineData)-1-i-1][2])
                    if oneDayLowPrice>float(klineData[len(klineData)-1-i-1][3]):
                        oneDayLowPrice = float(klineData[len(klineData)-1-i-1][3])

            INFO_ARR[index][4] = now

            oneDayWave = int(FUNCTION_CLIENT.get_percent_num(oneDayHighPrice-oneDayLowPrice,oneDayLowPrice))

            standardRate = oneDayWave/10*0.35

            if standardRate<STAND_LOW_RATE:
                standardRate = STAND_LOW_RATE

            print("standardRate:"+str(standardRate))
            INFO_ARR[index][3] = standardRate

            standardVol = threeDaysAllVol*0.125

            eightHoursVolA = 0
            for i in range(32):
                eightHoursVolA = eightHoursVolA+float(klineData[len(klineData)-1-i-1-16][7])

            eightHoursVolB = 0
            for i in range(32):
                eightHoursVolB = eightHoursVolB+float(klineData[len(klineData)-1-i-1][7])

            fourHoursVolA = 0
            for i in range(16):
                fourHoursVolA = fourHoursVolA+float(klineData[len(klineData)-1-i-1][7])

            if eightHoursVolA>=standardVol and eightHoursVolA>=80000000 and eightHoursVolB>=20000000:
                INFO_ARR[index][0] = 1
            else:
                INFO_ARR[index][0] = 0


            if eightHoursVolB>=20000000 and oneDayAllVol>100000000:
                INFO_ARR[index][1] = 1
            else:
                INFO_ARR[index][1] = 0

            if eightHoursVolB>=20000000 and oneDayAllVol>100000000:
                INFO_ARR[index][5] = 1
            else:
                INFO_ARR[index][5] = 0

            multiple = 1+ (eightHoursVolB)/20000000/10

            if multiple>2:
                multiple  = 2

            INFO_ARR[index][2]  = multiple
            inputData= json.dumps(INFO_ARR)
            with open('/var/www/html/vC.json', 'w',encoding='UTF-8') as fp:
                fp.write(inputData)
                fp.close()
    except Exception as e:
        FUNCTION_CLIENT.send_lark_msg_limit_one_min(str(e))
        print(e)
        time.sleep(0.5)
FUNCTION_CLIENT.send_lark_msg_limit_one_min("start")


while 1:
    FUNCTION_CLIENT.update_machine_status()
    getBTCRange()
    for index in range(len(TRADE_SYMBOL_ARR)):
        # print(TRADE_SYMBOL_ARR[index]["symbol"])
        updateVol(TRADE_SYMBOL_ARR[index]["symbol"],index)
        time.sleep(0.25)



