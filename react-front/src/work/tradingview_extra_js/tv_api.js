var TVjsApi = (function(){
    var TVjsApi = function(symbol) {
        let that = this
        that.updateIntervalTimer=()=>{}
        that.requestCompleteDataArr =[]
        that.tradeRecordArr = []
        that.nowShowTradeRecordCount = 0
        that.klineNowTs = 1600099200000
        that.updateInterval = 1000//历史回放的速度，单位毫秒
        that.nowAddKlineCount =0//历史回放已经播放的K线条数
        that.widgets = null;

        that.datafeeds = new datafeeds(that);
        that.symbol = symbol || 'ethusdt';
        that.interval = localStorage.getItem('tradingview.resolution') || '1';
        that.cacheData = {};
        that.lastTime = null;
        that.getBarTimer = null;
        that.isLoading = true;
        that.chartLoading = false
    }
    TVjsApi.prototype.init = function() {
        var resolution = this.interval;
        var chartType = (localStorage.getItem('tradingview.chartType') || '1')*1;

        var symbol = this.symbol;

        var locale = 'zh';

        var skin = localStorage.getItem('tradingViewTheme') || 'black';

        // var div = document.getElementById("kline_trade");
        // for(let a=0;a<100;a++){
        //     var newDiv=document.createElement("div");
        //     newDiv.id = "kline_trade_row_"+a.toString();
        //     newDiv.className = "kline-trade-row";
        //     div.appendChild(newDiv);
        //     let thisDiv=document.getElementById("kline_trade_row_"+a.toString());
        //
        //     var newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_trade_time_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-time";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_trade_price_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-price";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_trade_amount_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-amount";
        //     thisDiv.appendChild(newChildrenDiv);
        // }
        //
        // let depthSellDiv = document.getElementById("kline-depth-sell-row");
        // for(let a=0;a<10;a++){
        //     var newDiv=document.createElement("div");
        //     newDiv.id = "kline_depth_sell_row_"+a.toString();
        //     newDiv.className = "kline-depth-sell-row";
        //     depthSellDiv.appendChild(newDiv);
        //
        //     let thisDiv=document.getElementById("kline_depth_sell_row_"+a.toString());
        //     var newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_depth_sell_price_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-sell-price";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     var newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_depth_sell_amount_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-sell-amount";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     document.getElementById("kline_depth_sell_price_"+a.toString()).innerHTML="9494.94"
        //     document.getElementById("kline_depth_sell_amount_"+a.toString()).innerHTML="0.1000"
        // }
        //
        //
        // let depthBuyDiv = document.getElementById("kline-depth-buy-row");
        // for(let a=0;a<10;a++){
        //     var newDiv=document.createElement("div");
        //     newDiv.id = "kline_depth_buy_row_"+a.toString();
        //     newDiv.className = "kline-depth-buy-row";
        //     depthBuyDiv.appendChild(newDiv);
        //
        //     let thisDiv=document.getElementById("kline_depth_buy_row_"+a.toString());
        //     var newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_depth_buy_price_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-buy-price";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     var newChildrenDiv=document.createElement("div");
        //     newChildrenDiv.id = "kline_depth_buy_amount_"+a.toString();
        //     newChildrenDiv.className = "kline-trade-buy-amount";
        //     thisDiv.appendChild(newChildrenDiv);
        //
        //     document.getElementById("kline_depth_buy_price_"+a.toString()).innerHTML="9494.94"
        //     document.getElementById("kline_depth_buy_amount_"+a.toString()).innerHTML="0.1000"
        // }
        if (!this.widgets) {
            this.widgets = new TradingView.widget({
                autosize: true,
                symbol: symbol,
                interval: resolution,
                container_id: 'tv_chart_container',
                datafeed: this.datafeeds,
                library_path: 'charting_library/',
                enabled_features: [],
                timezone: 'Asia/Shanghai',
                // custom_css_url: './css/tradingview_'+skin+'.css',
                locale: locale,
                debug: false,
                disabled_features: [
                    "header_symbol_search",
                    "header_saveload",
                    "header_screenshot",
                    "header_chart_type",
                    "header_compare",
                    "header_undo_redo",
                    "timeframes_toolbar",
                    "volume_force_overlay",
                    "header_resolutions",
                ],
                //preset: "mobile",
                overrides: this.getOverrides(skin),
                studies_overrides: this.getStudiesOverrides(skin)
            })
            this.widgets.onChartReady(()=>{this.chartLoading=true})
            console.error(this.widgets)
            var thats = this.widgets;
            thats.onChartReady(function() {
                createStudy();
                createButton(buttons);
                thats.chart().setChartType(chartType);
                toggleStudy(chartType);
            })

            var buttons = [
                {title:'Time',resolution:'1',chartType:3},
                {title:'1min',resolution:'1',chartType:1},
                {title:'5min',resolution:'5',chartType:1},
                {title:'15min',resolution:'15',chartType:1},
                {title:'30min',resolution:'30',chartType:1},
                {title:'1hour',resolution:'60',chartType:1},
                {title:'1day',resolution:'1D',chartType:1},
                {title:'1week',resolution:'1W',chartType:1},
                {title:'1month',resolution:'1M',chartType:1},
            ];
            var studies = [];

            function createButton(buttons){
                for(var i = 0; i < buttons.length; i++){
                    (function(button){
                        thats.createButton()
                            .attr('title', button.title).addClass("mydate")
                            .text(button.title)
                            .on('click', function(e) {
                                if(this.parentNode.className.search('active') > -1){
                                    return false;
                                }
                                localStorage.setItem('tradingview.resolution',button.resolution);
                                localStorage.setItem('tradingview.chartType',button.chartType);
                                var $active = this.parentNode.parentNode.querySelector('.active');
                                $active.className = $active.className.replace(/(\sactive|active\s)/,'');
                                this.parentNode.className += ' active';
                                thats.chart().setResolution(button.resolution, function onReadyCallback() {});
                                if(button.chartType != thats.chart().chartType()){
                                    thats.chart().setChartType(button.chartType);
                                    toggleStudy(button.chartType);
                                }
                            }).parent().addClass('my-group'+(button.resolution==resolution && button.chartType == chartType ? ' active':''));
                    })(buttons[i]);
                }
            }
            function createStudy(){
                var id = thats.chart().createStudy('Moving Average', false, false, [5], null, {'Plot.color': 'rgb(150, 95, 196)'});
                studies.push(id);
                id = thats.chart().createStudy('Moving Average', false, false, [10], null, {'Plot.color': 'rgb(116,149,187)'});
                studies.push(id);
                id = thats.chart().createStudy('Moving Average', false, false, [20],null,{"plot.color": "rgb(58,113,74)"});
                studies.push(id);
                id = thats.chart().createStudy('Moving Average', false, false, [30],null,{"plot.color": "rgb(118,32,99)"});
                studies.push(id);
            }
            function toggleStudy(chartType){
                var state = chartType == 3 ? 0 : 1;
                for(var i = 0; i < studies.length; i++){
                    thats.chart().getStudyById(studies[i]).setVisible(state);
                }
            }
        }
    }
    TVjsApi.prototype.sortFun =function(a,b)
    {
        return  a['time']-b['time'] ;
    }
    TVjsApi.prototype.deepCopy =function(obj){
        var that = this
        var result = Array.isArray(obj) ? [] : {};
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (typeof obj[key] === 'object' && obj[key]!==null) {
                    result[key] = that.deepCopy(obj[key]);   //递归复制
                } else {
                    result[key] = obj[key];
                }
            }
        }
        return result;
    };
    TVjsApi.prototype.subscribe = function() {

    }

    TVjsApi.prototype.randomTradeRecord = function(lastPrice) {
        let directionRandom = Math.round(Math.random());
        let direction = "buy"
        if(directionRandom==0){
            direction = "sell"
        }

        let priceRandom = Math.random();
        let price = lastPrice
        if(directionRandom==0){
            direction = "sell"
        }

        return {
            'direction':direction,

        }
    }


    TVjsApi.prototype.beginInterval=function(interval){
        var input=document.getElementById("kline-speed-input");
        let newInerval = parseInt(input.value)
        if(!(!isNaN(newInerval)&&newInerval>0)){
            newInerval = 1000
        }
        let that = this
        let ticker = that.symbol + "-" + that.interval;
        clearInterval(that.updateIntervalTimer)
        that.updateIntervalTimer = setInterval(()=>{

            let newList=that.deepCopy(that.requestCompleteDataArr)
            let needKlineAmount = 0

            for(let a=0;a<newList.length;a++){
                if(newList[a]['time']<=that.klineNowTs){
                    needKlineAmount = a
                }else{
                    break
                }
            }
            newList = newList.splice(0,needKlineAmount+1)
            newList.sort(that.sortFun);
            let timeLen = that.interval*60*1000
            that.lastTime = newList[newList.length - 1].time
            let volumeCalculationBeginTs = that.lastTime
            let volumeCalculationEndTs = that.lastTime+timeLen
            let standardTradeRecordArr = []
            let thisIntervalVolume = 0
            let thisHigh = 0
            let thisLow = 99999
            for(let a=0;a<that.tradeRecordArr.length;a++){
                if(that.tradeRecordArr[a]['ts']<=that.klineNowTs){
                    standardTradeRecordArr.push({
                        'direction':that.tradeRecordArr[a]['direction'],
                        'time':that.tradeRecordArr[a]['time'],
                        'price':that.tradeRecordArr[a]['price'].toFixed(2),
                        'amount':that.tradeRecordArr[a]['amount'].toFixed(5)
                    })
                    if(standardTradeRecordArr.length>100){
                        standardTradeRecordArr.shift()
                    }
                }

                if(that.tradeRecordArr[a]['ts']<=that.klineNowTs&&that.tradeRecordArr[a]['ts']>volumeCalculationBeginTs){
                    thisIntervalVolume+=that.tradeRecordArr[a]['amount']
                    if(that.tradeRecordArr[a]['price']>thisHigh){
                        thisHigh = that.tradeRecordArr[a]['price']
                    }
                    if(that.tradeRecordArr[a]['price']<thisLow){
                        thisLow = that.tradeRecordArr[a]['price']
                    }
                }
            }
            standardTradeRecordArr = standardTradeRecordArr.reverse()
            for(let a=0;a<standardTradeRecordArr.length;a++){
                document.getElementById("kline_trade_time_"+a.toString()).innerHTML=standardTradeRecordArr[a]['time']
                document.getElementById("kline_trade_price_"+a.toString()).innerHTML=standardTradeRecordArr[a]['price']
                document.getElementById("kline_trade_price_"+a.toString()).className=standardTradeRecordArr[a]['direction']=="s"?"kline-trade-price-sell":"kline-trade-price-buy"
                document.getElementById("kline_trade_amount_"+a.toString()).innerHTML=standardTradeRecordArr[a]['amount']
            }
            if(newList.length>0&&standardTradeRecordArr.length>0){
                newList[newList.length-1]['close']=standardTradeRecordArr[0]['price']
                newList[newList.length-1]['volume']=thisIntervalVolume
                if(thisHigh!=0) {
                    newList[newList.length - 1]['high'] = thisHigh
                }
                if(thisLow!=99999){
                    newList[newList.length-1]['low']=thisLow
                }
                document.getElementById("kline-depth-price-row").innerHTML=standardTradeRecordArr[0]['price']
            }
            that.klineNowTs = that.klineNowTs +that.updateInterval
            document.getElementById("tv_chart_time").innerHTML= formatDate(new Date(that.klineNowTs),"C",(new Date()).valueOf())
            that.cacheData[ticker] = newList;
            that.datafeeds.barsUpdater.updateData()
            // },that.updateInterval)
        },newInerval)
    }
    TVjsApi.prototype.onMessage = function(data ) {
        var that = this
        let ticker = that.symbol + "-" + that.interval;
        if (data && data.length){
            //websocket返回的值，数组代表时间段历史数据，不是增量

            let list = []

            let tickerstate = ticker + "state";
            let tickerCallback = ticker + "Callback";
            var onLoadedCallback = that.cacheData[tickerCallback];
            // let onLoadedCallback = this.cacheData[tickerCallback];
            let completeList = []
            data.forEach((item,i)=>{
                if(item['id'] * 1000<that.klineNowTs) {
                    list.push({
                        time: item['id'] * 1000,
                        open: item['open'],
                        high: item['high'],
                        low: item['low'],
                        close: item['close'],
                        volume: item['amount']
                    })

                }
                completeList.push({
                    time: item['id'] * 1000,
                    open: item['open'],
                    high: item['high'],
                    low: item['low'],
                    close: item['close'],
                    volume: item['amount']
                })
            })

            list.sort(that.sortFun);
            that.requestCompleteDataArr =that.deepCopy(completeList)

            if(!that.cacheData[ticker]){
                that.cacheData[ticker] = list;
            }

            that.lastTime = that.cacheData[ticker][that.cacheData[ticker].length - 1].time
            if(onLoadedCallback) {
                onLoadedCallback(list);
                that.subscribe()
                that.cacheData[tickerstate] = !1;
                that.lastTime = that.cacheData[ticker][that.cacheData[ticker].length - 1].time
                that.beginInterval(100)
            }


        }

    }

    TVjsApi.prototype.reSetFlashSpeed = function() {

    }

    TVjsApi.prototype.subscribeBars= function(symbolInfo, resolution, onRealtimeCallback, subscriberUID, onResetCacheNeededCallback){

    }

    TVjsApi.prototype.initMessage = function(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback){
        var that = this
        var tickerCallback = this.symbol + "-" + resolution + "Callback";
        that.cacheData[tickerCallback] = onLoadedCallback;

        let request = new XMLHttpRequest();

        request.open("get", "https://zuibite-api.oss-cn-hongkong.aliyuncs.com/klineTest.json");/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            if (request.status == 200) {
                let data = JSON.parse(request.responseText);
                // message.success("读取数据成功"))
                this.onMessage(data)
                let tradeRequest = new XMLHttpRequest();

                tradeRequest.open("get", "https://zuibite-api.oss-cn-hongkong.aliyuncs.com/tradeTest.json");/*设置请求方法与路径*/
                tradeRequest.setRequestHeader("Cache-Control","no-cache");
                tradeRequest.setRequestHeader("Access-Control-Allow-Origin","*");
                tradeRequest.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
                tradeRequest.send(null);/*不发送数据到服务器*/
                tradeRequest.onload =()=> {
                    if (request.status == 200) {
                        let data = JSON.parse(tradeRequest.responseText);
                        let tradeRecordArr =[]
                        for(let a=0;a<data.length;a++){
                            tradeRecordArr.push({
                                'ts':parseInt(data[a][1]),
                                'time':formatDate(new Date(parseInt(data[a][1])),"M",(new Date()).valueOf()),
                                'price':parseFloat(data[a][2]),
                                'amount':parseFloat(data[a][3]),
                                'direction':data[a][4]
                            })
                        }
                        that.tradeRecordArr = tradeRecordArr
                    }
                }
            }

        }
    }

    TVjsApi.prototype.getBars = function(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback) {
        // console.log(' >> :', rangeStartDate, rangeEndDate)
        var that = this
        var ticker = that.symbol + "-" + resolution;
        var tickerload = ticker + "load";
        var tickerstate = ticker + "state";
        if(!that.cacheData[ticker] && !that.cacheData[tickerstate]){
            //如果缓存没有数据，而且未发出请求，记录当前节点开始时间
            that.cacheData[tickerload] = rangeStartDate;
            //发起请求，从websocket获取当前时间段的数据
            that.initMessage(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback);
            //设置状态为true
            that.cacheData[tickerstate] = !0;
            return false;
        }
        if(!that.cacheData[tickerload] || that.cacheData[tickerload] > rangeStartDate){
            // //如果缓存有数据，但是没有当前时间段的数据，更新当前节点时间
            // that.cacheData[tickerload] = rangeStartDate;
            // //发起请求，从websocket获取当前时间段的数据
            // that.initMessage(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback);
            // //设置状态为true
            // that.cacheData[tickerstate] = !0;
            // return false;
        }
        if(that.cacheData[tickerstate]){
            //正在从websocket获取数据，禁止一切操作
            return false;
        }
        ticker = that.symbol + "-" + that.interval;
        if (that.cacheData[ticker] && that.cacheData[ticker].length) {
            that.isLoading = false
            var newBars = []
            that.cacheData[ticker].forEach(item => {
                // if (item.time >= rangeStartDate * 1000 && item.time <= rangeEndDate * 1000) {
                newBars.push(item)
                // }
            })
            onLoadedCallback(newBars)
        } else {
            var self = that
            that.getBarTimer = setTimeout(function() {
                self.getBars(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback)
            }, 10)
        }
    }
    TVjsApi.prototype.getOverrides = function(theme){
        var themes = {
            "white": {
                up: "#03c087",
                down: "#ef5555",
                bg: "#ffffff",
                grid: "#f7f8fa",
                cross: "#23283D",
                border: "#9194a4",
                text: "#9194a4",
                areatop: "rgba(71, 78, 112, 0.1)",
                areadown: "rgba(71, 78, 112, 0.02)",
                line: "#737375"
            },
            "black": {
                up: "#589065",
                down: "#ae4e54",
                bg: "#181B2A",
                grid: "#1f2943",
                cross: "#9194A3",
                border: "#4e5b85",
                text: "#61688A",
                areatop: "rgba(122, 152, 247, .1)",
                areadown: "rgba(122, 152, 247, .02)",
                line: "#737375"
            },
            "mobile": {
                up: "#03C087",
                down: "#E76D42",
                bg: "#ffffff",
                grid: "#f7f8fa",
                cross: "#23283D",
                border: "#C5CFD5",
                text: "#8C9FAD",
                areatop: "rgba(71, 78, 112, 0.1)",
                areadown: "rgba(71, 78, 112, 0.02)",
                showLegend: !0
            }
        };
        var t = themes[theme];
        console.info(theme)
        console.info(t)
        return {
            "volumePaneSize": "medium",
            "scalesProperties.lineColor": t.text,
            "scalesProperties.textColor": t.text,
            "paneProperties.background": t.bg,
            "paneProperties.vertGridProperties.color": t.grid,
            "paneProperties.horzGridProperties.color": t.grid,
            "paneProperties.crossHairProperties.color": t.cross,
            "paneProperties.legendProperties.showLegend": !!t.showLegend,
            "paneProperties.legendProperties.showStudyArguments": !0,
            "paneProperties.legendProperties.showStudyTitles": !0,
            "paneProperties.legendProperties.showStudyValues": !0,
            "paneProperties.legendProperties.showSeriesTitle": !0,
            "paneProperties.legendProperties.showSeriesOHLC": !0,
            "mainSeriesProperties.candleStyle.upColor": t.up,
            "mainSeriesProperties.candleStyle.downColor": t.down,
            "mainSeriesProperties.candleStyle.drawWick": !0,
            "mainSeriesProperties.candleStyle.drawBorder": !0,
            "mainSeriesProperties.candleStyle.borderColor": t.border,
            "mainSeriesProperties.candleStyle.borderUpColor": t.up,
            "mainSeriesProperties.candleStyle.borderDownColor": t.down,
            "mainSeriesProperties.candleStyle.wickUpColor": t.up,
            "mainSeriesProperties.candleStyle.wickDownColor": t.down,
            "mainSeriesProperties.candleStyle.barColorsOnPrevClose": !1,
            "mainSeriesProperties.hollowCandleStyle.upColor": t.up,
            "mainSeriesProperties.hollowCandleStyle.downColor": t.down,
            "mainSeriesProperties.hollowCandleStyle.drawWick": !0,
            "mainSeriesProperties.hollowCandleStyle.drawBorder": !0,
            "mainSeriesProperties.hollowCandleStyle.borderColor": t.border,
            "mainSeriesProperties.hollowCandleStyle.borderUpColor": t.up,
            "mainSeriesProperties.hollowCandleStyle.borderDownColor": t.down,
            "mainSeriesProperties.hollowCandleStyle.wickColor": t.line,
            "mainSeriesProperties.haStyle.upColor": t.up,
            "mainSeriesProperties.haStyle.downColor": t.down,
            "mainSeriesProperties.haStyle.drawWick": !0,
            "mainSeriesProperties.haStyle.drawBorder": !0,
            "mainSeriesProperties.haStyle.borderColor": t.border,
            "mainSeriesProperties.haStyle.borderUpColor": t.up,
            "mainSeriesProperties.haStyle.borderDownColor": t.down,
            "mainSeriesProperties.haStyle.wickColor": t.border,
            "mainSeriesProperties.haStyle.barColorsOnPrevClose": !1,
            "mainSeriesProperties.barStyle.upColor": t.up,
            "mainSeriesProperties.barStyle.downColor": t.down,
            "mainSeriesProperties.barStyle.barColorsOnPrevClose": !1,
            "mainSeriesProperties.barStyle.dontDrawOpen": !1,
            "mainSeriesProperties.lineStyle.color": t.border,
            "mainSeriesProperties.lineStyle.linewidth": 1,
            "mainSeriesProperties.lineStyle.priceSource": "close",
            "mainSeriesProperties.areaStyle.color1": t.areatop,
            "mainSeriesProperties.areaStyle.color2": t.areadown,
            "mainSeriesProperties.areaStyle.linecolor": t.border,
            "mainSeriesProperties.areaStyle.linewidth": 1,
            "mainSeriesProperties.areaStyle.priceSource": "close"
        }
    }
    TVjsApi.prototype.getStudiesOverrides = function(theme){
        var themes = {
            "white": {
                c0: "#eb4d5c",
                c1: "#53b987",
                t: 70,
                v: !1
            },
            "black": {
                c0: "#fd8b8b",
                c1: "#3cb595",
                t: 70,
                v: !1
            }
        };
        var t = themes[theme];
        return {
            "volume.volume.color.0": t.c0,
            "volume.volume.color.1": t.c1,
            "volume.volume.transparency": t.t,
            "volume.options.showStudyArguments": t.v
        }
    }
    TVjsApi.prototype.resetTheme = function(skin){
        setTimeout(()=>{
            if(this.chartLoading){
                this.widgets.addCustomCSSFile('./css/tradingview_'+skin+'.css');
                this.widgets.applyOverrides(this.getOverrides(skin));
                this.widgets.applyStudiesOverrides(this.getStudiesOverrides(skin));
            }else{
                this.resetTheme(skin)
            }

        },100);

    }
    TVjsApi.prototype.formatt = function(time){
        if(isNaN(time)){
            return time;
        }
        var date = new Date(time);
        var Y = date.getFullYear();
        var m = this._formatt(date.getMonth());
        var d = this._formatt(date.getDate());
        var H = this._formatt(date.getHours());
        var i = this._formatt(date.getMinutes());
        var s = this._formatt(date.getSeconds());
        return Y+'-'+m+'-'+d+' '+H+':'+i+':'+s;
    }
    TVjsApi.prototype._formatt = function(num){
        return num >= 10 ? num : '0'+num;
    }
    return TVjsApi;
})();
