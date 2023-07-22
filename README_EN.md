# Introduction

It is the structure of Binance Futures, with a trading volume of more than 10 billion U.S. dollars and more than one year of real-time verification, including data, risk control, trading, and analysis, but does not include specific strategies.

Front-end demo: [8.217.121.203](http://8.217.121.203/), currently put 1000 US dollars to run a high-frequency left regression strategy with apr 100%~200%

You can use it to implement your transaction logic simply and at low cost. It uses a large number of Alibaba Cloud servers for distributed architecture, multi-process processing, and Lark for abnormal error reporting and transaction information disclosure.

If you are willing to read all the information in this readme in detail, especially [Module Detailed Analysis](#模块Detailed Analysis), then it will also be a book on Binance Contracts trading risk control, experience and understanding of the design architecture, and summarizes almost all my successes and failures.


# Advantage

Low cost, high efficiency, and simple implementation

With a cost of less than  150 USD per month, it can scan about 15 million symbol per minute to see if they meet the transaction conditions

Except for the matching server (C++), it is written in python, which is easy to understand

A large number of distributed architectures achieve faster speed, and the number of servers can be adjusted freely according to individual needs to achieve a balance between cost and performance

Read the market/account information through multiple interfaces and integrate it according to the update time stamp to minimize data risk

Enterprise-level risk control security solutions

# Architecture

The system uses a C++ server as the main matching server, and a large number of scalable and adjustable distributed python servers as data collection servers.

to feed the collected data, such as Kline, trades, tick, etc., to the C++ server.

The trading server then uniformly reads data from the C++ server, and maintains a K-line ledger on the local side to avoid the frequency limit of the exchange and achieve high-efficiency and low-cost data reading.

For another example, there are three ways to obtain the account balance and position data on Binance, a is position risk, b is account, and c is ws, then there will be three servers that use these three ways to read, and then import it to the C++ server for proofreading, intercept the latest data by comparing the update time, and then serve it to the trading server

The front-end data section uses Alibaba Cloud oss as an intermediary, and the web page reads oss data to display and isolate data risks

# Author

In 2021, I started quantitative trading after resigning from a top quantitative company. The main battlefield is Binance. In the past two years, I have been involved in various types of market maker->trend->arbitrage. At the peak, Binance had a monthly transaction volume of nearly 2 billion US dollars.

By July 2023, due to various reasons, the general direction has failed, leaving only a friend's funds to continue to operate a relatively stable and profitable left-hand trading strategy.

This is a set of high-efficiency, low-cost data reading and input framework that has been explored in the past two years. It also includes a set of risk control system. It is more like an architecture than an implementation. You can also apply it to okex, bybit, etc. through simple modification and replacement.

For financial cooperation or job opportunities (don’t talk about any strategy principles and source codes, please get straight to the point to save time for both parties), please email to c.binance.quant@gmail.com


# Environment and startup

The operating environment of our real project is Ubuntu 22.04 64-bit, Python 3.10.6

The python file runs in the following way, taking webServer as an example

```
ps -efwwww | grep webServer.py | awk '{print $2}' | xargs kill -9
dos2unix webServer.py
chmod +x webServer.py
nohup ./webServer.py >/dev/null &
```

But it is more recommended to use [dataPy/uploadDataPy](#dataPy/uploadDataPy)

React front-end project

```
npm install
```

```
npm start
```

C++ file

```
g++ wsServer.cpp -o wsServer.out -lboost_system
```

```
dos2unix wsServer.out
chmod +x wsServer.out
nohup ./wsServer.out >/dev/null &
```

Since all the libraries and packages used by the project are official or popular projects, you can find the installation method on Google, so I won’t repeat how to install the environment here

If you need the simplest startup solution, you can email us at c.binance.quant@gmail.com and share the system image directly to your Alibaba Cloud account, and charge 100 USDT for technical fees

# Module detailed analysis

The modules we designed include [General Part](#General Part), [Data Processing Part](#Data Processing Part), [Key Operation Part](#Key Operation Part), [Security Risk Control Part](#Security Risk Control Part), and specific transaction logic parts that are not open source

The minimum starting requirements of this project are a web server, a ws server, a tick data reading server, a one min kline data reading server, and a transaction server

You can expand related servers according to your own needs, for example, you need a 15 m kline, you need trades, etc., you only need to add on this basis, there is no integration of handicap data here, except buy one sell one.

For higher-dimensional handicap data, we choose to read it in the trading server

Because apart from kline data, the integration of other data does not have much practical significance

The kline data of 200 trading pairs can reduce the frequency of calling the interface in this way, and the latest data can still be obtained through proofreading when some interfaces are delayed

But there is only one API for handicap data, so there is no integration requirement.

Our solution to the delay of handicap data is through the distributed operation of transaction servers.

For example, five trading servers are set up, running the same logic of opening and closing positions. After the pre-opening conditions are met, the five servers will simultaneously enter the process of reading handicap data, and read the same data in multiple processes at the same time, which can optimize delays and other unexpected situations.

By the way, here is a way for a transaction server to issue an order.

There are two types, one is to issue directly on the transaction server, and the other is to make a web server that issues transaction instructions, and the transaction server sends a unified request to the intranet web server through http requests.

For example, five trading servers, assuming that the total transaction volume demand is 100u, then each server is responsible for 20u of transaction volume, if there is a delay or other problems, if a server loses the signal, it will lose 20u of transaction volume

And if the web server is used to send out uniformly, then 100% of the transaction volume will be issued when the http request is received for the first time

The two methods have their own applicable places and advantages, and you need to choose by yourself. In fact, the second method has been integrated in the webserver file.


The specific server configuration of the real project currently maintained by us is (the server name is the name of the open source file, and there is a more detailed introduction to individual files below)

A wsPosition server, used to read the position and balance data of Binance through ws, and import it into the ws data matching server

A positionRisk server, which is used to read the /fapi/v2/positionRisk interface, obtain position information through this interface and judge the loss in real time, so as to stop the loss in time. This server has similar functions to wsPosition, makerStopLoss, and getBinancePosition. The reason why multiple servers with the same functions are designed is to prevent risks to the greatest extent. In the event of a delay in a certain interface of Binance, the system can still run robustly, and will not be repeated below.

A makerStopLoss server is used to read the individual pending order information after reading the position information from the getBinancePosition server, and then preset the stop loss order. The reason why it is split from the getBinancePosition server is because the weight required to read the pending order is higher, splitting into two IPs can be operated at a higher frequency

A getBinancePosition server, used to read the /fapi/v2/account interface, obtain the position information and balance, and import it to the ws data matching server

A commission server for recording flow information

A checkTimeoutOrders server, used to read the /fapi/v1/openOrders interface, query all pending orders, and then cancel the pending orders exceeding a certain period of time, or perform some additional operations, for example, if the pending order is not eaten within three seconds, it will be converted into a take order, etc.

A cancelServer server, which is essentially a web server server, runs the webServer file to cancel the order

A webServer server, which is essentially a web server server, runs the webServer file, which is used for most programs to read transaction pairs at the beginning, etc.

Two oneMinKlineToWs servers, used for low-frequency reading of one-minute line klines

Two volAndRate servers, used to read transaction volume data for analysis and provide to other servers

Ten specialOneMinKlineToWs servers for high-frequency reading of one-minute klines

Ten tickToWs servers for reading tick group information

A ws server, used for C++ data stamping server

And five trading servers, in addition to running the trading program and running the webServer at the same time, provide an interface for checkTimeout to obtain all pending order data

A total of 38 servers, and a mysql database with a minimum configuration

Among them, for the opening server and ws server, the server with high main frequency is selected, and the speed is about doubled. It is not necessary to perform this optimization for other market and data entry servers, only need to choose the preemptive server with the lowest configuration

The comprehensive cost is less than 3,000 RMB per month, and the bulk is in the traffic fee. Personally, I think that cutting the above amount in half can still meet most quantitative risk control and delay needs.


In this project, a single module requires one server and one IP to run independently. At present, the https reading frequency of a single module has basically been tuned to the maximum value allowed by Binance.

What needs to be explained here is that Alibaba Cloud Tokyo is used as an example here, and Binance’s servers are in Amazon Cloud Tokyo.

The delay described in this article actually includes two delays, one is the delay of reading frequency, and the other is the delay of the network. After the comprehensive calculation of these two delays, it is the final delay in the real environment.

The reason why Alibaba Cloud is used is because Alibaba Cloud's preemptive servers have cost advantages and thus have the advantage of reading frequency delay.

Alibaba Cloud's network delay is about 10ms, while Amazon is expected to be 1~3ms without applying for intranet permissions. Applying for intranet will face the problem of locking ip, that is, it is impossible to reduce the delay by spreading more ip.

Although the Amazon cloud has lower latency, but due to

1. The ws-type data read is usually locked by Binance with a delay of more than 100ms, and the ws-type read data has some unconfirmable risk factors, so this method is excluded

2. If the https reading method is used, the reading weight of some data is as high as 20, or even 30. From this, it is deduced that multiple IPs are needed, and distributed reading can have higher frequency. At this time, the cost price of a single IP becomes a factor that needs to be considered. The cost of Alibaba Cloud's preemptive server is less than 2 usd a month. After comprehensive cost-effective considerations, we chose Japan's Alibaba Cloud.

3. This solution is not a solution for high-frequency (nanosecond-level) transactions, otherwise it will all be written in C++. In fact, it is a set of solutions that pursue cost, delay, and development speed, and balance the optimal solution among the three, and serve millisecond-level strategies

## Common section

### react_front folder

The front-end file, the webpage is an external webpage, so the time interval of one minute is forced to be locked, and the displayed data is relatively simple, after all, it is external

I also designed a detailed data analysis website on the intranet, but this part actually needs to be customized with its own quantitative strategy, and once it is made public, there is a risk of strategy leakage, so it will not be disclosed here.

In addition, the data processing after the transaction and the front-end code are all based on the realization of functions, so they do not pay attention to other indicators such as performance, please refer to the FAQ at the bottom

### afterTrade folder

How to update the server to the front-end data file, the main principle is to use Alibaba Cloud oss as middleware to isolate data risks

Among them, tradesUpdate.py is a more detailed trade record, you need to call the begin_trade_record interface of webServer to insert the transaction data when placing an order

Please note that the design of this interface is based on my own needs, because everyone has different quantitative models, parameters, etc., and needs to study differently, so I suggest you rewrite this piece yourself

positionRecord.py mainly records the account balance and position value per minute, serving the following files

webOssUpdate.py will organize the data and upload it to oss, and the web front end will read the data from oss, and will organize the transaction records to form a statistical table in units of days. This place simply counts the profit and handling fee, and you can expand it yourself.

### binance_f folder

Binance's processing package related to the API key interface is a version that has undergone secondary transformation after downloading it from github recommended by Binance's official website

###config.py

General configuration, you need to configure the mysql database by yourself, and apply for the Lark api key, etc.

### commonFunction.py

general method

### updateSymbol/trade_symbol.sql

Generate the trade_symbol table in the database, which will control the trading pair information of the system that can execute the transaction

### updateSymbol/updateTradeSymbol.sql

Enter the transaction pair information into the trade_symbol table

Some special processing has been carried out here, mainly to adapt to our situation, including only entering usdt trading pairs, not entering index-type trading pairs (such as btcdom, football, etc.)

Most of the fields here are designed to cooperate with another project, professional manual tools, and the data fields used for quantification are actually only symbol, status

### simpleTrade

A most basic trading demonstration program, when a certain trading pair has a position value of 0 and a one-minute increase > 1%, open a long position, and when his position value > 0 and a one-minute decline is less than -0.5%

If you are a novice, it is recommended to pay attention to the updateSymbolInfo() function, price accuracy, quantity accuracy, and the maximum number of liquidated positions should be the most common problems that novices will encounter.

## Data processing part

### wsServer.cpp

matching server

All data will be imported here, and some multi-source data will judge whether to update the data according to the update timestamp of the data. Use the following command line to compile it into an executable file

g++ wsServer.cpp -o wsServer.out -lboost_system

The source code uses two libraries, one is websocketpp and the other is boost

### dataPy/uploadDataPy

Upload the program from an Alibaba Cloud master server to each corresponding Alibaba Cloud server, run it, and then destroy it.

Here only show the use of three data entry programs, tick, oneMinKlineToWs, specialOneMinKlineToWs, other programs are the same

The program can simply and quickly release distributed running programs, and run and destroy them on the cloud on all servers that meet the naming rules.

Before use, you need to name the Alibaba Cloud server uniformly, such as tickToWs_1, tickToWs_2...

Before using, upload the file locally to a master server, and then run the program on the master server. After normal operation, all hard disks including the master server and the actual running server should be overwritten with the information of the source file.

The program will call the get_aliyun_private_ip_arr_by_name function to search for the private network address of the Alibaba Cloud server in the corresponding character field, upload it, execute it, and judge whether it is running normally after three seconds

If it is running normally, the hard disk data will be overwritten and destroyed afterwards to prevent confidential data from leaking, and only the program will be kept running in the memory

Since it is an operation of a private network address, the program needs to be executed on the Alibaba Cloud server in the same region

### dataPy/oneMinKlineToWs.py

The program belongs to the distributed operation architecture, and only needs standardized naming to expand the server infinitely and reduce the delay
![image](https://github.com/Melelery/c-binance-future-quant/assets/139823868/801409a3-25b7-41c8-b795-d7aa0efd0fe6)

Slowly updated 1-minute K-line data reading program

Every time the program runs, it will send the total number of current transaction pairs to the ws server.

Every time before reading kline data, a transaction pair number will be obtained from the ws server. At the same time, the ws server will perform a +1 operation on the number to ensure that when the distributed architecture is used, each extended oneMinKlineToWs can read the kline data of the transaction pair in the best order.

Since Binance’s k-line data update delay is slightly higher than that of tick data, the k-line data comes from the database, and the tick data comes from the cache. At the same time, the delay of a single symbol will be lower than the information of all transaction pairs, so each transaction will be read again before each update to correct the last k-line data.

The kline data will send data to the ws server twice, once for all the read data. For example, when reading the kline, set limit=45, that is, read the data of the latest 45 klines, but obviously, the data of the first 43 items are always unchanged, so the transaction server only needs a long time (30 seconds/1 minute...) to correct once. Only the latest two data have a high probability of change and need to be read in real time.

So I split it into two pieces of information, one is the first two klines, and the other is all klines. The first two klines are used for real-time reading by the trading server.

Reducing the length of the message will greatly help the time it takes for the trade server to parse the message.

The k-line at other time intervals, such as 5 minutes, 15 minutes, 1 hour, etc., is also the same as the process of reading and entering the ws server. It can be realized by simply replacing the parameters in the file, so it will not be listed here

### dataPy/specialOneMinKlineToWs.py

The program belongs to the distributed operation architecture, and only needs standardized naming to expand the server infinitely and reduce the delay

Quickly updated 1-minute K-line data reading program

The difference from the above is that the reading data here has a pre-trading volume condition. You can understand that my quantitative system will only open a position when it meets the requirements of a certain trading volume condition. Therefore, for this part of the trading pairs that may open a position, a server dedicated to reading data has been laid.

Assuming that there were originally 200 trading pairs read in turn, after the restriction, it becomes 20 trading pairs, which means that the data read data of your single machine has increased by 10 times

This is just a display program. In fact, you should write corresponding conditions according to your trading conditions to limit the trading pairs for data reading.

The k-line at other time intervals, such as 5 minutes, 15 minutes, 1 hour, etc., is also the same as the process of reading and entering the ws server. It can be realized by simply replacing the parameters in the file, so it will not be listed here

### dataPy/tickToWs.py

The program belongs to the distributed operation architecture, and only needs standardized naming to expand the server infinitely and reduce the delay

The tick data reading program will read the number of all tick servers on Alibaba Cloud, and then automatically lock the server for data reading within a certain period of time within one second

For example, now we have opened five tick servers, then the tick 1 server will read data within the period of >=0 <200 milliseconds per second, and the tick 2 will read data within the period of >=200 <400 milliseconds per second...and so on

After the tick data is imported into the ws server, the trading program reads this part and mainly uses it to correct the highest price, the lowest price and the latest price of the latest kline.

###dataPy/useData.py

It shows how to get the one min kline data and tick data from the ws server, and how to combine them locally to maintain a k-line data. Here, it can also be extended to add data such as trade vol. The principle is the same, so it will not be shown again

## Key operation part

### binanceOrdersRecord.py

Record orders information to facilitate subsequent analysis, for example, you can analyze the total transaction ratio of outgoing orders through the records of orders, etc.

### binanceTradesRecord.py

Record trades information to facilitate subsequent analysis, for example, the total transaction volume can be calculated through trades, etc.

### checkTimeoutOrders.py

Check if there is an overtime order and cancel it. At the same time, some transaction operations can be added. For example, if the maker’s pending order exceeds the number of seconds without a transaction, it will be converted into a take order in proportion

Because it is necessary to call the api of Binance to obtain all pending orders, and the api has a very high weight, in order to meet more sensitive scanning, my five trading servers run webserver programs at the same time, and checkTimeoutOrders will read all pending orders from the five trading servers in turn.

###commission.py

Record all capital flows, this is the most important data, through which you can calculate the handling fee, profit, capital cost and other data

Due to the large amount of data accumulated by the commission for a long time, there are two tables here, one is a continuous recording table, and the other is a 24-hour temporary recording table.

The temporary table recorded for 24 hours is mainly used to analyze the loss situation of the latest day, so as to control the risk of the trading system

For example, the following code
```
for key in fourHoursProfitObj:
     if fourHoursProfitObj[key]<=-150 or oneDayProfitObj[key]<=-1800:
         banSymbolArr.append(key)

if allOneDayProfit<=-3000:
     banSymbolArr = ["ALL"]
```
When the four-hour profit of a trading pair is less than 150u or the 24-hour profit is less than 1800u, it will send a list of prohibited trading pairs to the ws server. When the total profit of all trading pairs is less than -3000u, all transactions will be suspended directly.

### getBinancePosition.py

Obtain Binance position and balance information through the /fapi/v2/account interface, and upload it to port 80 of this server, and ws service

The information uploaded to the ws server will be compared with the update timestamp of the information obtained by positionRisk and wsPosition, and the latest information will be selected and sent to the transaction server

Other servers read json files through port 80 to obtain data. The scheme used in the old version uses ws later, but it is retained here

### positionRisk.py

Obtain Binance position and balance information through the /fapi/v2/positionRisk interface, and the others are the same as above

### wsPosition.py

Obtain Binance position and balance information through the websocket interface, and the others are the same as above

###makerStopLoss

After reading the position information from the ws server, read the Binance interface pending order information of the currency. The reason why all symbol pending order information is not used is because the weight is too high, which will cause the stop loss to be too slow.

When the maximum value of the position changes by more than 5%, the maximum stop loss order is placed. The presentation file is written with 5% of the cost price as the initial stop loss price, and it is split into five orders, and the price of each order is increased by 0.5% for stop loss to prevent the impact of depth

Example: The current position is 1000u, and there is a stop loss order. When the position increases to 1001u, the system will not reset the stop loss, because it does not satisfy the situation that the quantity changes > 5%. Too sensitive reset will cause weight loss and other problems

If it is increased to 1060u, then five stop loss orders will be reset. The initial stop loss price is 5% of the cost price, and each subsequent stop loss order is 5.5%, 6%, 6.5%, 7%,

After the new stop loss is set, the system will read the pending order to check whether it is successful, and the old stop loss order will be canceled only after the confirmation is successful.


## Security risk control part

Since the source code of the program will contain sensitive information, it is recommended to use the dataPy/uploadDataPy upload method to upload, run, and destroy the file in a unified manner, so that it can only run in the memory and cover all the program information stored on the hard disk, and only keep the source code in the local segment.

It is recommended to close all external ports of Alibaba Cloud. When purchasing a server, choose to place all servers under the unified private network prefix IP, so that the functions can be operated normally and communicate with each other while closing the external network port. If it is not under the unified private network prefix IP, you need to add the corresponding private network IP to the security group of some servers

When you need to operate the server, add the local IP to the security group, and delete it immediately after use

It is recommended to bind Binance's api to the IP of the server

It is recommended to keep the operating system updated

# FAQ

## 1. Why not backtest with historical data first

In fact, it has been three years since I personally explored and quantified.

The method of fitting a broken line after backtesting with historical data is not untried.

However, it may be more difficult for the backtest environment to be consistent with the real offer than most people currently estimate. What I mean by consistency is absolute consistency. Any small difference will actually be magnified throughout the whole process to an unacceptable level in the end.

And there is a problem that it is impossible to verify whether the difference in profit or loss is caused by errors or strategies.

Because it is very likely that by the time you end the project, there will still be dozens of errors that you have not discovered, and it is not possible to quantify the possibility of determining the profit and loss caused by these errors.

Of course, this is a conclusion based on my ability and perspective.

So since the last six months, my thinking has been to go directly to the real offer, even if it is a small fund verification, and adjust the parameters based on the data of the real offer

## 2. There is some possibility of performance improvement

Yes, since this is a personal project, I have a lot going on.

So for some places that do not need to pursue performance, I will use the simplest way of writing.

For example, orders and trades are entered into the database by comparing the latest 1,000 data, and inserting if there are no duplicates. Of course, there is a way of writing with better performance, but it doesn’t make much sense to me, so I didn’t spend time improving it.

Why it doesn't make much sense, because the ratio of cpu and memory usage did not exceed 50% during the operation of the entire mysql system with the lowest configuration.

Most of my energy is focused on data entry and transaction performance optimization, ignoring the optimization of post-transaction data pull analysis, as long as the final result is correct.

The process after the transaction, whether it consumes 1 performance or 100 performances, as long as it does not reach the peak value of my hardware, I will not seek to change it
