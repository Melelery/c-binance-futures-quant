'use strict';

var _dataUpdater2 = _interopRequireDefault(dataUpdater);

var LastLength;

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } } /**
                                                                                                                                                           * JS API
                                                                                                                                                           */
var datafeeds = function () {

  /**
   * JS API
   * @param {*Object} vue vue实例
   */
  function datafeeds(vue) {
    _classCallCheck(this, datafeeds);

    this.self = vue;
    this.barsUpdater = new _dataUpdater2.default(this);
  }

  /**
   * @param {*Function} callback  回调函数
   * `onReady` should return result asynchronously.
   */


  datafeeds.prototype.onReady = function onReady(callback) {
    var _this = this;

    return new Promise(function (resolve, reject) {
      var configuration = _this.defaultConfiguration();
      if (_this.self.getConfig) {
        configuration = Object.assign(_this.defaultConfiguration(), _this.self.getConfig());
      }
      resolve(configuration);
    }).then(function (data) {
      return callback(data);
    });
  };

  /**
   * @param {*String} symbolName  商品名称或ticker
   * @param {*Function} onSymbolResolvedCallback 成功回调 
   * @param {*Function} onResolveErrorCallback   失败回调
   * `resolveSymbol` should return result asynchronously.
   */


  datafeeds.prototype.resolveSymbol = function resolveSymbol(symbolName, onSymbolResolvedCallback, onResolveErrorCallback) {
    var _this2 = this;

    return new Promise(function (resolve, reject) {
      var symbolInfo = _this2.defaultSymbol();
      if (_this2.self.getSymbol) {
        symbolInfo = Object.assign(_this2.defaultSymbol(), _this2.self.getSymbol());
      }
      resolve(symbolInfo);
    }).then(function (data) {
      return onSymbolResolvedCallback(data);
    }).catch(function (err) {
      return onResolveErrorCallback(err);
    });
  };

  /**
   * @param {*Object} symbolInfo  商品信息对象
   * @param {*String} resolution  分辨率
   * @param {*Number} rangeStartDate  时间戳、最左边请求的K线时间
   * @param {*Number} rangeEndDate  时间戳、最右边请求的K线时间
   * @param {*Function} onDataCallback  回调函数
   * @param {*Function} onErrorCallback  回调函数
   */


  datafeeds.prototype.getBars = function getBars(symbolInfo, resolution, rangeStartDate, rangeEndDate, onDataCallback, onErrorCallback) {
    var onLoadedCallback = function onLoadedCallback(data) {
                //if(data&&LastLength!=data.length){
                if(data&&data.length){
                        onDataCallback(data, { noData: false });
                 }else{
                         onDataCallback([], { noData: true });
                }
                 LastLength = data.length;

 

//或者可以这样写： data && data.length ? onDataCallback(data, { noData: true }) : onDataCallback([], { noData: true });
    };
    this.self.getBars(symbolInfo, resolution, rangeStartDate, rangeEndDate, onLoadedCallback);
  };

  /**
   * 订阅K线数据。图表库将调用onRealtimeCallback方法以更新实时数据
   * @param {*Object} symbolInfo 商品信息
   * @param {*String} resolution 分辨率
   * @param {*Function} onRealtimeCallback 回调函数 
   * @param {*String} subscriberUID 监听的唯一标识符
   * @param {*Function} onResetCacheNeededCallback (从1.7开始): 将在bars数据发生变化时执行
   */


  datafeeds.prototype.subscribeBars = function subscribeBars(symbolInfo, resolution, onRealtimeCallback, subscriberUID, onResetCacheNeededCallback) {
    this.barsUpdater.subscribeBars(symbolInfo, resolution, onRealtimeCallback, subscriberUID, onResetCacheNeededCallback);
  };

  /**
   * 取消订阅K线数据
   * @param {*String} subscriberUID 监听的唯一标识符
   */


  datafeeds.prototype.unsubscribeBars = function unsubscribeBars(subscriberUID) {
    this.barsUpdater.unsubscribeBars(subscriberUID);
  };

  /**
   * 默认配置
   */


  datafeeds.prototype.defaultConfiguration = function defaultConfiguration() {
      //设置默认配置
    return {
      supports_search: false,
      supports_group_request: false,
      supported_resolutions: ['1', '5', '15', '30', '60', '1D', '1W', '1M'],
      supports_marks: true,
      supports_timescale_marks: true,
      supports_time: true
    };
  };

  /**
   * 默认商品信息
   */


  datafeeds.prototype.defaultSymbol = function defaultSymbol() {
    return {
      'name': this.self.symbol.toLocaleUpperCase(),
      'timezone': 'Asia/Shanghai',
      'minmov': 1,
      'minmov2': 0,
      'pointvalue': 1,
      'fractional': false,
      //设置周期
      'session': '24x7',
      'has_intraday': true,
      'has_no_volume': false,  
       //设置是否支持周月线
       "has_daily":true,
       //设置是否支持周月线
       "has_weekly_and_monthly":true,
      'description': this.self.symbol.toLocaleUpperCase(),
          //设置精度  100表示保留两位小数   1000三位   10000四位
      'pricescale': 100,
      'ticker': this.self.symbol.toLocaleUpperCase(),
      'supported_resolutions': ['1', '5', '15', '30', '60', '240','1D', '5D', '1W', '1M']
    };
  };

  return datafeeds;
}();
