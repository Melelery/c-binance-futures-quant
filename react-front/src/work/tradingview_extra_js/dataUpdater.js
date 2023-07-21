'use strict';


function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * 数据更新器
 * 通过更新器触发datafeeds的getBars实时更新图表数据
 */
var dataUpdater = function () {
  function dataUpdater(datafeeds) {
    _classCallCheck(this, dataUpdater);

    this.subscribers = {};
    this.requestsPending = 0;
    this.historyProvider = datafeeds;
  }

  dataUpdater.prototype.subscribeBars = function subscribeBars(symbolInfo, resolution, newDataCallback, listenerGuid) {
    this.subscribers[listenerGuid] = {
      lastBarTime: null,
      listener: newDataCallback,
      resolution: resolution,
      symbolInfo: symbolInfo
    };
  };

  dataUpdater.prototype.unsubscribeBars = function unsubscribeBars(listenerGuid) {
    delete this.subscribers[listenerGuid];
  };

  dataUpdater.prototype.updateData = function updateData() {
    var _this = this;

    if (this.requestsPending) return;
    this.requestsPending = 0;
    for (var listenerGuid in this.subscribers) {
      this.requestsPending++;
      this.updateDataForSubscriber(listenerGuid).then(function () {
        return _this.requestsPending--;
      }).catch(function () {
        return _this.requestsPending--;
      });
    }
  };

  dataUpdater.prototype.updateDataForSubscriber = function updateDataForSubscriber(listenerGuid) {
    var _this2 = this;

    return new Promise(function (resolve, reject) {
      var subscriptionRecord = _this2.subscribers[listenerGuid];
      var rangeEndTime = parseInt((Date.now() / 1000).toString());
      var rangeStartTime = rangeEndTime - _this2.periodLengthSeconds(subscriptionRecord.resolution, 10);
      _this2.historyProvider.getBars(subscriptionRecord.symbolInfo, subscriptionRecord.resolution, rangeStartTime, rangeEndTime, function (bars) {
        _this2.onSubscriberDataReceived(listenerGuid, bars);
        resolve();
      }, function () {
        reject();
      });
    });
  };

  dataUpdater.prototype.onSubscriberDataReceived = function onSubscriberDataReceived(listenerGuid, bars) {
    if (!this.subscribers.hasOwnProperty(listenerGuid)) return;
    if (!bars.length) return;
    var lastBar = bars[bars.length - 1];
    var subscriptionRecord = this.subscribers[listenerGuid];
    if (subscriptionRecord.lastBarTime !== null && lastBar.time < subscriptionRecord.lastBarTime) return;
    var isNewBar = subscriptionRecord.lastBarTime !== null && lastBar.time > subscriptionRecord.lastBarTime;
    if (isNewBar) {
      if (bars.length < 2) {
        throw new Error('Not enough bars in history for proper pulse update. Need at least 2.');
      }
      var previousBar = bars[bars.length - 2];
      subscriptionRecord.listener(previousBar);
    }

    subscriptionRecord.lastBarTime = lastBar.time;
    subscriptionRecord.listener(lastBar);
  };

  dataUpdater.prototype.periodLengthSeconds = function periodLengthSeconds(resolution, requiredPeriodsCount) {
    var daysCount = 0;
    if (resolution === 'D' || resolution === '1D') {
      daysCount = requiredPeriodsCount;
    } else if (resolution === 'M' || resolution === '1M') {
      daysCount = 31 * requiredPeriodsCount;
    } else if (resolution === 'W' || resolution === '1W') {
      daysCount = 7 * requiredPeriodsCount;
    } else {
      daysCount = requiredPeriodsCount * parseInt(resolution) / (24 * 60);
    }
    return daysCount * 24 * 60 * 60;
  };

  return dataUpdater;
}();