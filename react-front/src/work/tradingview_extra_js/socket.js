'use strict';


function _classCallCheck(instance, Constructor) { 
    if (!(instance instanceof Constructor)) 
    { throw new TypeError("Cannot call a class as a function"); 
    } 
}

var socket = function () {
  function socket() {
    var url = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 'wss://api.fcoin.com/v2/ws';
    var options = arguments[1];

    _classCallCheck(this, socket);

    this.heartBeatTimer = null;
    this.options = options;
    this.messageMap = {};
    this.connState = 0;
    this.socket = null;
    this.url = url;
  }

  socket.prototype.doOpen = function doOpen() {
    var _this = this;
    console.log("我被调用了")
    if (this.connState) return;
    this.connState = 1;
    this.afterOpenEmit = [];
    var BrowserWebSocket = window.WebSocket || window.MozWebSocket;
    var socket = new BrowserWebSocket(this.url);
    socket.binaryType = 'arraybuffer';
    socket.onopen = function (evt) {
      return _this.onOpen(evt);
    };
    socket.onclose = function (evt) {
      return _this.onClose(evt);
    };
    socket.onmessage = function (evt) {
      return _this.onMessage(evt.data);
    };
    socket.onerror = function (err) {
      return _this.onError(err);
    };
    this.socket = socket;
  };

  socket.prototype.onOpen = function onOpen(evt) {
    this.connState = 2;
    this.heartBeatTimer = setInterval(this.checkHeartbeat.bind(this), 20000);
    this.onReceiver({ Event: 'open' });
  };

  socket.prototype.checkOpen = function checkOpen() {
    return this.connState === 2;
  };

  socket.prototype.onClose = function onClose() {
    this.connState = 0;
    if (this.connState) {
      this.onReceiver({ Event: 'close' });
    }
  };

  socket.prototype.send = function send(data) {    
    if(this.socket.readyState != 1){
      console.log('readyState',this.socket.readyState)
      setTimeout(function(){
        this.send(data);
      }.bind(this),100);
    }else{
      this.socket.send(JSON.stringify(data));
    }
    
  };

  socket.prototype.emit = function emit(data) {
    var _this2 = this;

    return new Promise(function (resolve) {
      _this2.socket.send(JSON.stringify(data));
      _this2.on('message', function (data) {
        resolve(data);
      });
    });
  };

  socket.prototype.onMessage = function onMessage(message) {
    try {
      var data = JSON.parse(message);
      this.onReceiver({ Event: 'message', Data: data });
    } catch (err) {
      console.error(' >> Data parsing error:', err);
    }
  };

  socket.prototype.checkHeartbeat = function checkHeartbeat() {
    var data = {
      'cmd': 'ping',
      'args': [Date.parse(new Date())],
      'id': '1368'
    };
    this.send(data);
  };

  socket.prototype.onError = function onError(err) {};

  socket.prototype.onReceiver = function onReceiver(data) {
    var callback = this.messageMap[data.Event];
    if (callback) callback(data.Data);
  };

  socket.prototype.on = function on(name, handler) {
    this.messageMap[name] = handler;
  };

  socket.prototype.doClose = function doClose() {
    this.socket.close();
  };

  socket.prototype.destroy = function destroy() {
    if (this.heartBeatTimer) {
      clearInterval(this, this.heartBeatTimer);
      this.heartBeatTimer = null;
    }
    this.doClose();
    this.messageMap = {};
    this.connState = 0;
    this.socket = null;
  };

  return socket;
}();