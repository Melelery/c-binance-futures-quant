# Introduction

At present, the high-frequency system code and ideas that I am running in real trading have been made public. Please visit http://melelery.com for details.

It is the structure of Binance Futures, with more than $10 billion in trading volume and more than a year of real-time verification, including data entry, risk control, trading, data analysis, but does not include specific strategies.

You can use it to implement your trading logic in a simple, low-cost way, which makes extensive use of AliCloud servers for distributed architecture, multi-processing, and Flybook for exception reporting and transaction information disclosure.

If you are willing to read all the information in this readme in detail, especially [Module Detailed Analysis](#Module-detailed-analysis), then it will also be a book on Binance Contracts trading risk control, experience and understanding of the design architecture, and summarizes almost all my successes and failures.

I track the skeleton of the strategy I maintain, under different parameters and factors of the live real-time trading display page

Updating these languages below is scheduled for the 27th of August 2023

In all honesty, I don't want to make the project public, and the most important thing you want when doing quantisation, especially in the cryptocurrency world, is to keep a low profile

The purpose of my posting a series of Zhihu articles and open sourcing on github in July 2023 was because I had, in the past year, suffered the biggest Waterloo of my life, I was heavily in debt and had no choice but to seek out collaborations for a shot at survival

I did get cooperation opportunities through this project, including funds and accounts, as well as a lot of friends doing high-frequency, in the mutual exchanges between the formation of a lot of inspiration for me, and integrated into my actual strategy and structure, I think these two months is the two months of my history, the fastest growth in quantitative aspects!

As a result of my first time open sourcing, I accidentally compromised my personal confidence in the project and was attacked by a social worker, but the cost, including the value I brought to other people by open sourcing, was fair compared to what I got out of it!

I am still grateful, so although I have got what I wanted, I will not delete the project and all the articles, now or in the future!

The high-frequency system I am currently running is based on this project, but the actual latency has been optimised to less than a tenth of the open-source architecture, and will not be open-sourced, nor will the project be updated.


My other articles

[10ms, python+aliyun, not beautiful, but practical](https://zhuanlan.zhihu.com/p/647402709)

[Exploration of a self-built high-frequency simulation aggregation engine](https://zhuanlan.zhihu.com/p/646840989)

[Exchange Interface Latency Analysis](https://zhuanlan.zhihu.com/p/647035185)

my high-frequency live 
[C Quant club] (http://c-quant.club/#/CQuant)

Receive funds, 20,000 U.S. dollars to 500,000 U.S. dollars, the estimated annualized 100% ~ 150%, 5 5 points, loss is responsible for, the maximum retracement of 30%, at least six months of the signing, the end of the month, the need to call my account, to provide data web page, interested in contacting the WeChat melelery

# Advantage

Low cost, high efficiency and simple implementation are the three advantages of this system.

With a cost of less than 1,000 RMB a month, it can scan about 15 million pairs per minute to see if the trading conditions are met.

All but the aggregation server (C++) are written in python, which is easy to understand.

Massively distributed architecture to achieve faster speeds, and the number of servers can be freely scaled according to individual needs to achieve a balance between cost and performance.

Read quotes/account information through multiple interfaces and integrate them according to update timestamps to minimise data risk.

Enterprise-level risk control and security solutions

# Architecture

The system works through a C++ server as the main aggregation server and a large number of scalable and adjustable distributed python servers as data collection servers.

The collected data, including Kline , trades, ticks, etc., are fed to the C++ server.

The trading server then reads the data uniformly from the C++ server and maintains a Kline book on the local side to avoid the frequency limitation of the exchange and achieve high efficiency and low cost data reading.

For example, there are three ways to get the account balance and position data on CoinAn, a is position risk, b is account, c is ws, then there will be three servers to read the data in these three ways, and then converge to the C++ server for proofreading, and then intercept the latest data by comparing with the update time, and then serve it to the trading server.

Front-end data board, through the Ali cloud oss as an intermediary, the web page to read oss data for display, isolate the data risk


# Environment and startup

Our live project runs on Ubuntu 22.04 64-bit, Python 3.10.6.

The python files are run in the following way, using the webServer as an example

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

Since all the libraries and packages used in the project are official or popular projects, you can find the installation method in google, so I won't repeat how to install the environment here.

If you need a minimal startup solution, you can contact us at c.binance.quant@gmail.com and we will share the system image directly to your Aliyun account for a technical fee of 1000 USDT.

# Module detailed analysis

The modules we designed include [General Part](#General Part), [Data Processing Part](#Data Processing Part), [Key Operation Part](#Key Operation Part), [Security Risk Control Part](#Security Risk Control Part), and specific transaction logic parts that are not open source


The minimum requirements for this project are a web server, a ws server, a tick data reading server, a one min kline data reading server, and a trades server.

You can expand the servers according to your needs, e.g. if you need a 15 m kline, trades, etc., just add on top of that, there is no integration of the handicap data, except for the buy one sell one.

For higher dimensions of intraday data, we choose to read it inside the trading server.

Because there is not much point in integrating other data except kline data.

With 200 pairs of kline data, this way we can reduce the frequency of interface calls and still get the latest data by proofreading even if some interfaces have delays.

But there is only one api for handicap data, so there is no need for integration.

Our solution for the latency of the handicap data is through the distributed operation of the trading servers.

If you set up five trading servers, running the same opening and closing logic, after meeting the pre-opening conditions, the five servers will simultaneously enter the process of opening and reading data, the same time multiple processes to read the same data, you can optimise the delay and other unexpected conditions.

Here incidentally leads to a trading server to issue orders.

There are two kinds, one is issued directly on the trading server, one is to make a trading order issued by the web server, the trading server through http request to the intranet web server after the unified issue.

For example, five trading servers, assuming that the total volume demand is 100u, then each server is responsible for 20u of the transaction volume, if the delay or other problems, a server lost the signal that is the loss of 20u of the transaction volume.

If a web server is used to send out a unified request, then 100% of the volume will be sent out the first time a http request is received.

Both ways have their own advantages and applicability, you need to choose, in fact, in the webserver file has been integrated into the second way.


We are currently maintaining the real project, the specific server configuration is, (server name is the open source file name, in the following there is a more detailed description of the individual files)

A wsPosition server, used to read the position and balance data of CoinOn through ws, and remit them to the ws data aggregation server.

A positionRisk server, used to read /fapi/v2/positionRisk interface, through the interface to obtain position information and real-time judgement of the loss, in order to facilitate timely stop-loss, the server and wsPosition, makerStopLoss, getBinancePosition have similar functions. The reason for designing multiple servers with the same functionality is to maximise the risk of the system remaining robust in the event of a delay in one of CoinSecure's interfaces, which will not be repeated below.

A makerStopLoss server is used to read the position information from the getBinancePosition server, then read the separate pending order information, and then preset the stop loss order. The reason for splitting with the getBinancePosition server is that reading the pending order requires higher weight, and splitting into two ips allows for a higher frequency of the operation

One getBinancePosition server, used to read /fapi/v2/account interface, get the position information and balance and then remit to the ws data aggregation server.

A commission server to record the flow information.

A checkTimeoutOrders server, which is used to read /fapi/v1/openOrders interface, query all pending orders, and then cancel the pending orders that have exceeded a certain period of time, or carry out some additional operations, for example, if a pending order is not eaten for three seconds, it will be converted into a take order and so on.

A cancelServer server, which is essentially a web server server, running webServer files for cancelling orders.

One webServer server, which is also essentially a web server server, running the webServer file, which is used to read trade pairs at the beginning of most programmes, etc.

Two oneMinKlineToWs servers for low frequency reading of one minute line klines.

Two volAndRate servers, used to read volume data for analysis and to provide to other servers.

Ten specialOneMinKlineToWs servers for high-frequency reading of one-minute klines.

Ten tickToWs servers for reading tick group information.

one ws server for C++ data stamping server

and five trading servers, which run the webServer in addition to the trading programme and provide an interface to checkTimeout to get all the pending order data.

Total 38 servers, and a mysql database with minimum configuration.

For the open position server and ws server, we chose a high-frequency type of server, about double the speed increase, the other quotes and data entry servers do not need to carry out this optimisation, only the lowest configuration of the preemptive server.

Comprehensive cost of less than 3000 RMB a month, the big head in the traffic costs, I think the above number of half cut can still meet most of the quantitative wind control and latency needs.


In that project, a separate module, need a server and an IP to run separately, has basically tuned the https read frequency of a single module to the maximum allowed by CoinSecure.

It should be noted here that here are all to AliCloud Tokyo as an example, CoinSecurity's servers in the Amazon cloud Tokyo.

The latency described in this article, in fact, contains two kinds of latency, one is the latency of the read frequency, and the other is the latency of the network, the two kinds of latency combined calculation is the final latency in the real environment.

The reason why we use Aliyun is because Aliyun preemptive servers have a cost advantage, and thus have the advantage of reading frequency latency.

Aliyun network latency is about 10ms, while Amazon is expected to be 1~3ms without applying for intranet access, and applying for intranet faces the problem of locking the ip, i.e. it is not possible to reduce the latency by means of spreading more ip.

Although Amazon cloud has lower latency, due to

1. ws-type data reading is usually locked by CoinSecurity with a latency of more than 100ms, and ws-type data reading has certain risk factors that cannot be confirmed, so this method is ruled out.

2. if you take https reading method, some data reading weight up to 20, or even 30, which deduced the need for multi-IP, distributed reading to have a higher frequency, and at this time, the cost of a single IP price that becomes a factor to consider, Aliyun preemptive server cost less than 20 yuan a month, in the comprehensive cost-effective considerations, we chose the After considering the overall cost-effectiveness, we chose Aliyun Japan.

3. This solution is not a solution for high frequency (nanosecond level) trading, otherwise it would be written in C++, in fact, it is a solution that pursues the optimal balance of cost, latency, and development speed, and serves millisecond level strategies.


## General section

### react_front folder

The front-end file, the webpage is an external webpage, so it is forced to lock the time interval of one minute, and the data displayed is relatively simple, after all, it is an external webpage.

I have also designed a detailed data analysis website for the intranet, but this part actually needs to be customised according to your own quantitative strategy, and there is a risk of strategy leakage once it is made public, so it is not disclosed here.

In addition, the after trade data processing, as well as the front-end code, are all based on the implementation of the function, so do not focus on other indicators such as performance, you can refer to the bottom faq

### afterTrade folder

How the server updates to the front-end data files, the main principle is to use AliCloud oss as middleware, isolate the data risk

The tradesUpdate.py is a more detailed trade record, which requires you to call the webServer's begin_trade_record interface to insert the trade data when placing an order.

Please note that the design of this interface is based on my own needs, because everyone's quantitative models, parameters, etc. are different, and need to study is not the same, so it is recommended that this piece of their own rewriting

positionRecord.py mainly records the account balance and position value per minute, serving the following files

webOssUpdate.py will collate the data and upload it to oss, the web front-end will read the data from oss, and will collate the transaction flow record to form a statistical table in terms of days, the service is just a simple statistic of the profit and commission, you can expand it by yourself.

### binance_f folder

The processing package for the interface involving the api key, downloaded from github recommended by the official website of Binance, is the version that has been remodelled twice.

### config.py

Common configuration, need to configure mysql database, and apply for Flybook api key, etc.

### commonFunction.py

Common methods

### updateSymbol/trade_symbol.sql

Generate the trade_symbol table in the database, which will control the pair information of the system's executable trades.

### updateSymbol/updateTradeSymbol.sql

Entering trade pair information into the trade_symbol table

There is some special handling here, mainly to suit our situation, including only entering usdt pairs and not index pairs (e.g. btcdom, football).

Most of the fields here are designed to work with another project, the Professional Handler, and the only data fields used for quantitative purposes are actually symbol and status.

### simpleTrade

A basic trading demo, open long when a pair has a position value of 0 and a one-minute gain of >1%, close long when it has a position value of >0 and a one-minute loss of less than -0.5%.

If you are a novice, it is recommended to pay attention to updateSymbolInfo () this function, price accuracy, quantity accuracy, the maximum number of closed positions should be a novice will encounter the most problems.

## Data processing section

### wsServer.cpp

Summary Server

All data will be aggregated here, some multi-source data will be updated according to the update timestamps that come with the data to determine whether to update that piece of data, using the following command line can be compiled into an executable file

g++ wsServer.cpp -o wsServer.out -lboost_system

The source code uses two libraries, one for websocketpp and one for boost.

### dataPy/uploadDataPy

Uploads the application from a single AliCloud master server to each corresponding AliCloud server, runs it, and then destroys it.

Only tick, oneMinKlineToWs and specialOneMinKlineToWs are shown here, and the same applies to other apps.

This procedure can be simple and fast release of distributed running procedures to all servers that meet the naming rules on the cloud run and destroy.

Before using it, you need to unify the AliCloud servers into a unified name, such as tickToWs_1,tickToWs_2...

Before use, upload files from local to one of the master servers, then run the program on the master server, after normal operation, including the master server and the actual running server on all the hard drives should be overwritten with the information of the source file.

The program will call the get_aliyun_private_ip_arr_by_name function to search for the private address of the Aliyun server in the corresponding character segment, then upload it, execute it, and judge whether it is running normally after three seconds.

If it is running normally, it will overwrite and destroy the data on the hard disc to prevent confidential data leakage, and only keep the programme running in the memory.

Since this is a private address operation, it is necessary to execute the programme on the AliCloud server in the same region.

### dataPy/oneMinKlineToWs.py

The program is a distributed operation architecture, only need to standardise the naming can be unlimited expansion of servers to reduce latency
! [image](https://github.com/Melelery/c-binance-future-quant/assets/139823868/801409a3-25b7-41c8-b795-d7aa0efd0fe6)

Slowly updating 1-minute K-line data readers

Each time the program runs, it sends the total number of current pairs to the ws server.

Every time before reading kline data, it will get a pair number from ws server, while taking it, ws server will perform +1 operation on the number to make sure that in distributed architecture, every extension oneMinKlineToWs can read kline data of pairs in the best order.

Since CoinSecurity's kline data update latency is slightly higher than tick data, kline data is sourced from the database while tick data is sourced from the cache, and the latency of a single symbol is lower than that of all the pair information, the pair's individual tick data will be read again before each update to correct the last kline data.

The kline data will be sent to the ws server twice, once for all the data read, for example, when reading the kline, set limit=45, that is, read the last 45 kline data, but obviously, the data of the previous 43 is always the same, so the trading server will only need to take a long time (30 seconds / 1 minute...) Only the latest two data have a high probability of change and need to be read in real time.

So I split it into two messages, one for the first two klines and one for all klines. The first two klines are used for real-time reading and real-time updating by the trading server, while the last two ends are used for calibration after a certain time interval.

Reducing the length of the message is extremely helpful for the time used by the trading server to parse the message.

Other time intervals, such as 5 minutes, 15 minutes, 1 hour, etc., can also be read and entered into the ws server in the same way, simply by replacing the parameters in the file, so they are not listed here.

### dataPy/specialOneMinKlineToWs.py

This program is a distributed operation architecture, just need to standardise the naming can be infinitely scalable servers to reduce latency

Rapidly updating 1-minute K-line data readers.

Unlike the above, the reading of data here has a pre-volume condition, you can understand that my quantitative system will only open a position if it meets the requirements of a certain volume condition, so for this part of the trading pairs that may open a position, laying a special server to read the data.

Suppose there were 200 trading pairs to read in turn, after the restriction, it becomes 20 trading pairs, then it is equal to your individual machine data reading data increased by 10 times!

This is only a demonstration of the programme, in fact, you should be based on your trading conditions to write their own conditions, to limit the data read by the trading pairs.

Other time intervals such as 5 mins, 15 mins, 1 hour, etc. can be read and fed into the ws server in the same way, by simply replacing the parameters in the file, so they are not listed here.

### dataPy/tickToWs.py

This is a distributed architecture, so it only needs standardised naming to scale servers infinitely and reduce latency.

The tick data reading program will read all the tick servers on AliCloud, and then automatically lock the servers to read the data within a certain period of time within one second.

Let's say we have five tick servers up and running, then tick 1 will read the data in the >=0 < 200 milliseconds time period every second, tick 2 will read the data in the >=200 < 400 milliseconds time period every second... And so on.

After the tick data is imported to the ws server, the trader reads this part mainly for correcting the highest, lowest and latest price of the latest kline.

### dataPy/useData.py

shows how to take one min kline data and tick data from the ws server, and then put them together locally to maintain a kline data, which can be extended to include trade vol and other data, the principle is the same, so we don't show it again.

## Key operations section

### binanceOrdersRecord.py

Record the orders information for subsequent analysis, for example, you can use the orders record to analyse the total percentage of outgoing orders and so on.

### binanceTradesRecord.py

Record trades information for subsequent analysis, e.g. total volume can be calculated from the trades record, etc.

### checkTimeoutOrders.py

Checks if there are timeout orders and cancels them, at the same time you can attach some trading operations, such as maker pending orders for more than a number of seconds without a transaction will be converted into a proportional take orders

Since you need to call CoinSafe's api to get all pending orders, and the weight of this api is very high, in order to meet the more sensitive scanning, my five trading servers are running webserver programs at the same time, checkTimeoutOrders will take turns to read all the pending orders from the five trading servers.

### commission.py

Records all the money flow, this is the most important data, through which you can calculate the commission, profit, capital costs and so on.

Because of the large amount of data accumulated by commission over a long period of time, there are two tables here, one for continuous recording and one for 24-hour temporary recording.

The 24-hour temporary table is mainly used to analyse the latest day's losses, so as to give the trading system for risk control.

For example, this code
``
for key in fourHoursProfitObj:: if fourHoursProfitObj
    if fourHoursProfitObj[key]<=-150 or oneDayProfitObj[key]<=-1800:: banSymbolArr[key]<=-150
        banSymbolArr.append(key)

if allOneDayProfit<=-3000: banSymbolArr.append(key).
    banSymbolArr = ["ALL"]
``
When a pair is read with a four-hour profit of less than 150u or a 24-hour profit of less than 1800u, a list of forbidden pairs is sent to the ws server, and when the total profit of all pairs is less than -3000u, all trading is suspended directly.

### getBinancePosition.py

Get Binance position and balance information through the /fapi/v2/account interface and upload it to port 80 of this server and the ws service.

The information uploaded to the ws server will be compared with the updated timestamps of the positionRisk and wsPosition information, and the latest information will be selected and sent to the trading server.

The other servers read the json file on port 80 to get the data, the old version of the scheme, later adopted the ws but retained here

### positionRisk.py

Get position and balance information via /fapi/v2/positionRisk interface, same as above.

### wsPosition.py

Get position and balance information via websocket interface, same as above.

### makerStopLoss

After reading the position information, the ws server reads the CoinSafe interface pending order information for that coin. The reason why we don't use pending order information for all symbols is because the weight is too high, which can cause the stop loss to be too sluggish.

At the same time as the maximum value of the position has changed by more than 5%, the maximum stop-loss order is hung, the demo file is written to 5% of the cost price as the initial stop-loss price, and split into five orders, each order to increase the price of the stop-loss backward by 0.5%, to prevent the impact of the depth of the

Example: Now the position is 1000u, there is a stop loss order, then when the position is increased to 1001u, the system will not reset the stop loss, because it does not meet the number of changes > 5%, too sensitive to reset the weight will be consumed and so on.

If it increases to 1060u, then it will reset five stop-loss orders, the initial stop-loss price is 5% of the cost price, and each subsequent stop-loss order will be 5.5%, 6%, 6.5%, 7%, in that order.

After the new stop loss is set, the system will read the pending order to check if it is successful, and only after confirming the success will the old stop loss order be cancelled.


## Security and wind control part

As the source code of the programme will carry sensitive information, it is recommended to use the upload method of dataPy/uploadDataPy to unify the uploading, running and destroying of the files, so as to achieve the purpose of running in the memory only and covering all the stored programme information in the hard disk, and keeping the source code in the local section only.

It is recommended to close all external ports of Aliyun, and put all servers under the unified private prefix IP when purchasing servers, so that normal operation and interoperability can be achieved while closing external ports, if not under the unified private prefix IP, then you need to add the corresponding private IP to the security group of some servers.

When you need to operate the server, add the local IP to the security group, and delete it immediately after use.

It is recommended that CoinSafe's api binds to the server's IP.

It is recommended to keep the operating system up-to-date.

# FAQ

## 1. Why don't you use historical data to backtest first?

In fact, I have been exploring quantitative research for three years.

It is not true that I haven't tried to fit a line out after backtesting with historical data.

But backtesting the environment to do with the real market consistent with the difficulty may exceed the current estimates of most people, I said consistent is absolutely consistent, any small differences in the whole process will actually be amplified to the extent that you can not accept the end.

And there is the problem of not being able to verify whether the difference in profit and loss is due to error or strategy.

Because it is very likely that by the time you finish the project, there will still be dozens of places where you did not find errors, and do not have the possibility of quantitatively judging the profit and loss caused by these errors.

Of course this is a conclusion based on my ability and perspective.

So since the last six months, my thinking is directly on the real market, even if it is a small amount of money to verify the data based on the real market to adjust the reference

## 2. Partially there is the possibility of performance improvement

Yes, because this is a personal project, I have to be responsible for a lot of things.

So for some places where I don't need to pursue performance, I will use the simplest way to write them.

For example, orders and trades are entered into the database by comparing the last 1,000 entries and inserting any duplicates. Of course, there is a better way to write this, but it doesn't make a lot of sense to me, so I didn't take the time to improve it.

Why is not significant, because I use the lowest configuration mysql whole system running process cpu and memory use ratio is not more than 50%.

Most of my energy is focused on data entry, transaction performance optimisation, while ignoring the post-transaction data pulling and analysis of the optimisation of this piece, this piece as long as the final result is right.

The post-trade process, whether it consumes 1 performance or 100, as long as it doesn't reach the peak of my hardware, I'm not looking to change it!
