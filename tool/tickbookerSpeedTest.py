#!/usr/bin/python3.10
# encoding:utf-8
import time
import requests
import json
import random
import traceback
import _thread
from config import *
from commonFunction import FunctionClient

lastTsA = 0

lastTsB = 0

minDelayTs = 9999999999999

REQUESTS_SESSION = requests.Session()

beginTs  = int(time.time()*1000)
for i in range(100):
	url = "https://fapi.binance.com/fapi/v1/trades?symbol=BTCUSDT"
	tickerData =  json.loads(REQUESTS_SESSION.get(url,timeout=(1,1)).content.decode())
	nowTs = tickerData[b]["time"]
	for b  in range(len(tickerData)):
		if tickerData[b]["time"]>nowTs:
			nowTs= tickerData[b]["time"]

	tsDifferent = 999999999
	print("------------------")
	print(nowTs - lastTsA)
	print( lastTsA - lastTsB)
	if nowTs - lastTsA!=0 and lastTsA - lastTsB !=0:
		tsDifferent = nowTs - lastTsA
		if nowTs - lastTsA < lastTsA - lastTsB:
			tsDifferent =  lastTsA - lastTsB
	if tsDifferent <minDelayTs :
		minDelayTs= tsDifferent
	lastTsB = lastTsA
	lastTsA = nowTs

endTs  = int(time.time()*1000)

print(minDelayTs)
print(endTs - beginTs)