#!/usr/bin/python3.10
# coding=utf-8

import sys
import json
import random
import time
import requests
import oss2
import socket
import decimal
import datetime
import string

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="updateTradeSymbol",connectMysql =True)

sql = "truncate table trade_symbol" 
FUNCTION_CLIENT.mysql_commit(sql,[])

url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
response = requests.request("GET", url,timeout=(3,7)).json()
symbolsArr = response["symbols"]

#update symbol
for a in range(len(symbolsArr)):
    if  symbolsArr[a]["status"]=="TRADING" and symbolsArr[a]["deliveryDate"]==4133404800000 and symbolsArr[a]["underlyingType"]!="INDEX"  and symbolsArr[a]["quoteAsset"]=="USDT":
        thisSymbol = symbolsArr[a]["symbol"]
        thisBaseAsset = symbolsArr[a]["baseAsset"]
        thisQuote = thisSymbol.replace(thisBaseAsset,"")
        sql = "INSERT INTO trade_symbol ( symbol,`coin`,`quote`,`status`,`onboardDate`,`index`,`defaultShow`,`onboardTs`,`linkSymbolArr`)  VALUES ( %s, %s,%s,%s, %s,%s,%s, %s,%s );" 
        FUNCTION_CLIENT.mysql_commit(sql,[thisSymbol,thisBaseAsset,thisQuote,"yes",turnTsToTime(int(symbolsArr[a]["onboardDate"]/1000)),0,0,int(symbolsArr[a]["onboardDate"]/1000),json.dumps([])])


url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
response = requests.request("GET", url,timeout=(3,7)).json()
oneDayVolArr = response
for i in range(len(oneDayVolArr)):
    symbol = oneDayVolArr[i]["symbol"]
    sql = "update trade_symbol set `quoteVolume`=%s where symbol =%s" 
    FUNCTION_CLIENT.mysql_commit(sql,[oneDayVolArr[i]["quoteVolume"],symbol])

print("update index")
#update index
sql = "select `id` from trade_symbol where `status`='yes' order by id asc" 
tradeSymbolData = FUNCTION_CLIENT.mysql_select(sql,[])
for i in range(len(tradeSymbolData)):
    sql = "update trade_symbol set `index`=%s where id =%s" 
    FUNCTION_CLIENT.mysql_commit(sql,[i,tradeSymbolData[i][0]])


#update default show
coinArr = []
sql = "select `coin` from trade_symbol where `status`='yes' order by id asc" 
tradeSymbolData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tradeSymbolData)):
    coinInCoinArr = False
    for b in range(len(coinArr)):
        if coinArr[b] == tradeSymbolData[a][0]:
            coinInCoinArr = True
    if not coinInCoinArr:
        coinArr.append(tradeSymbolData[a][0])

for a in range(len(coinArr)):
    thisCoin = coinArr[a]
    sql = "select `onboardTs`,`symbol`,`id`,`coin`,`index` from trade_symbol where coin=%s order by `quoteVolume` desc" 
    tradeSymbolData = FUNCTION_CLIENT.mysql_select(sql,[thisCoin])
    for b in range(len(tradeSymbolData)):
        thisId = tradeSymbolData[b][2]
        if b==0:
            sql = "update trade_symbol set `defaultShow`=1 where `id`=%s " 
            FUNCTION_CLIENT.mysql_commit(sql,[thisId])
        else:
            sql = "update trade_symbol set `defaultShow`=0 where `id`=%s " 
            FUNCTION_CLIENT.mysql_commit(sql,[thisId])


#update link symbol arr
coinArr = []
sql = "select `symbol`,`id`,`coin`,`index` from trade_symbol order by id asc" 
tradeSymbolData = FUNCTION_CLIENT.mysql_select(sql,[])
for a in range(len(tradeSymbolData)):
    thisCoin = tradeSymbolData[a][2]
    thisId = tradeSymbolData[a][1]
    sql = "select `symbol` from trade_symbol where coin=%s" 
    tradeSymbolDataB = FUNCTION_CLIENT.mysql_select(sql,[thisCoin])
    linkSymbolArr = []
    for b in range(len(tradeSymbolDataB)):
        linkSymbolArr.append(tradeSymbolDataB[b][0])
    sql = "update trade_symbol set `linkSymbolArr`=%s where `id`=%s " 
    FUNCTION_CLIENT.mysql_commit(sql,[json.dumps(linkSymbolArr),thisId])
