import threading
import websocket
import gzip
import ssl
import logging
from urllib import parse
import urllib.parse

from binance_f.base.printtime import PrintDate
from binance_f.impl.utils.timeservice import get_current_timestamp
from binance_f.impl.utils.urlparamsbuilder import UrlParamsBuilder
from binance_f.impl.utils.apisignature import create_signature
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.impl.utils import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
# Key: ws, Value: connection
websocket_connection_handler = dict()


def on_message(ws, message):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_message(message)
    return


def on_error(ws, error):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_failure(error)


def on_close(ws):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_close()


def on_open(ws):
    websocket_connection = websocket_connection_handler[ws]
    websocket_connection.on_open(ws)


connection_id = 0


class ConnectionState:
    IDLE = 0
    CONNECTED = 1
    CLOSED_ON_ERROR = 2


def websocket_func(*args):
    connection_instance = args[0]
    connection_instance.ws = websocket.WebSocketApp(connection_instance.url,
                                                    on_message=on_message,
                                                    on_error=on_error,
                                                    on_close=on_close)
    global websocket_connection_handler
    websocket_connection_handler[connection_instance.ws] = connection_instance
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connecting...")
    connection_instance.delay_in_second = -1
    connection_instance.ws.on_open = on_open
    connection_instance.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connection event loop down")
    if connection_instance.state == ConnectionState.CONNECTED:
        connection_instance.state = ConnectionState.IDLE


class WebsocketConnection:

    def __init__(self, api_key, secret_key, uri, watch_dog, request):
        self.__thread = None
        self.url = uri
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.request = request
        self.__watch_dog = watch_dog
        self.delay_in_second = -1
        self.ws = None
        self.last_receive_time = 0
        self.logger = logging.getLogger("binance-futures")
        self.state = ConnectionState.IDLE
        global connection_id
        connection_id += 1
        self.id = connection_id

    def in_delay_connection(self):
        return self.delay_in_second != -1

    def re_connect_in_delay(self, delay_in_second):
        if self.ws is not None:
            self.ws.close()
            self.ws = None
        self.delay_in_second = delay_in_second
        self.logger.warning("[Sub][" + str(self.id) + "] Reconnecting after "
                            + str(self.delay_in_second) + " seconds later")

    def re_connect(self):
        if self.delay_in_second != 0:
            self.delay_in_second -= 1
            self.logger.warning("In delay connection: " + str(self.delay_in_second))
        else:
            self.connect()

    def connect(self):
        if self.state == ConnectionState.CONNECTED:
            self.logger.info("[Sub][" + str(self.id) + "] Already connected")
        else:
            self.__thread = threading.Thread(target=websocket_func, args=[self])
            self.__thread.start()

    def send(self, data):
        self.ws.send(data)

    def close(self):
        self.ws.close()
        del websocket_connection_handler[self.ws]
        self.__watch_dog.on_connection_closed(self)
        self.logger.error("[Sub][" + str(self.id) + "] Closing normally")

    def on_open(self, ws):
        self.logger.info("[Sub][" + str(self.id) + "] Connected to server")
        self.ws = ws
        self.last_receive_time = get_current_timestamp()
        self.state = ConnectionState.CONNECTED
        self.__watch_dog.on_connection_created(self)
        if self.request.subscription_handler is not None:
            self.request.subscription_handler(self)
        return

    def on_error(self, error_message):
        if self.request.error_handler is not None:
            print('error')
            exception = BinanceApiException(BinanceApiException.SUBSCRIPTION_ERROR, error_message)
            self.request.error_handler(exception)
        self.logger.error("[Sub][" + str(self.id) + "] " + str(error_message))

    def on_failure(self, error):
        print('on_failure')
        self.on_error("Unexpected error: " + str(error))
        self.close_on_error()

    def on_message(self, message):
        self.last_receive_time = get_current_timestamp()
        json_wrapper = parse_json_from_string(message)

        if json_wrapper.contain_key("status") and json_wrapper.get_string("status") != "ok":
            error_code = json_wrapper.get_string_or_default("err-code", "Unknown error")
            error_msg = json_wrapper.get_string_or_default("err-msg", "Unknown error")
            self.on_error(error_code + ": " + error_msg)
        elif json_wrapper.contain_key("err-code") and json_wrapper.get_int("err-code") != 0:
            error_code = json_wrapper.get_string_or_default("err-code", "Unknown error")
            error_msg = json_wrapper.get_string_or_default("err-msg", "Unknown error")
            self.on_error(error_code + ": " + error_msg)
        elif json_wrapper.contain_key("result") and json_wrapper.contain_key("id"):
            self.__on_receive_response(json_wrapper)
        else:
            self.__on_receive_payload(json_wrapper)

    def __on_receive_response(self, json_wrapper):
        res = None
        try:
            res = json_wrapper.get_int("id")
        except Exception as e:
            self.on_error("Failed to parse server's response: " + str(e))

        try:
            if self.request.update_callback is not None:
                self.request.update_callback(SubscribeMessageType.RESPONSE, res)
        except Exception as e:
            self.on_error("Process error: " + str(e)
                     + " You should capture the exception in your error handler")

    def __on_receive_payload(self, json_wrapper):
        res = None
        try:
            if self.request.json_parser is not None:
                res = self.request.json_parser(json_wrapper)
        except Exception as e:
            self.on_error("Failed to parse server's response: " + str(e))

        try:
            if self.request.update_callback is not None:
                self.request.update_callback(SubscribeMessageType.PAYLOAD, res)
        except Exception as e:
            self.on_error("Process error: " + str(e)
                     + " You should capture the exception in your error handler")

        if self.request.auto_close:
            self.close()

    def __process_ping_on_trading_line(self, ping_ts):
        self.send("{\"op\":\"pong\",\"ts\":" + str(ping_ts) + "}")
        return

    def __process_ping_on_market_line(self, ping_ts):
        self.send("{\"pong\":" + str(ping_ts) + "}")
        return

    def close_on_error(self):
        if self.ws is not None:
            self.ws.close()
            self.state = ConnectionState.CLOSED_ON_ERROR
            self.logger.error("[Sub][" + str(self.id) + "] Connection is closing due to error")
