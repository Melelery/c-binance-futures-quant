import requests
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.impl.utils import *
# from binance_f.base.printobject import *


def check_response(json_wrapper):
    if json_wrapper.contain_key("success"):
        success = json_wrapper.get_boolean("success")
        if success is False:
            err_code = json_wrapper.get_int_or_default("code", "")
            err_msg = json_wrapper.get_string_or_default("msg", "")
            if err_code == "":
                raise BinanceApiException(BinanceApiException.EXEC_ERROR, "[Executing] " + err_msg)
            else:
                raise BinanceApiException(BinanceApiException.EXEC_ERROR, "[Executing] " + str(err_code) + ": " + err_msg)
    elif json_wrapper.contain_key("code"):
        code = json_wrapper.get_int("code")
        msg = json_wrapper.get_string_or_default("msg", "")
        if code != 200:
            raise BinanceApiException(BinanceApiException.EXEC_ERROR, "[Executing] " + str(code) + ": " + msg)

def get_limits_usage(response):
    limits = {}
    limits_headers = ["X-MBX-USED-WEIGHT-", "X-MBX-ORDER-COUNT-" ]  # Limit headers to catch
    for key,value in response.headers.items():
        if any([key.startswith(h) for h in limits_headers]):
            limits[key] = value
    return limits

def call_sync(request):
    if request.method == "GET":
        response = requests.get(request.host + request.url, headers=request.header,timeout=(5,5))
        return response.text
    elif request.method == "POST":
        response = requests.post(request.host + request.url, headers=request.header,timeout=(5,5))
        print(response)
        return response.text
    elif request.method == "DELETE":
        response = requests.delete(request.host + request.url, headers=request.header,timeout=(5,5))
        limits = get_limits_usage(response)
        json_wrapper = parse_json_from_string(response.text)
        print(response.text)
        check_response(json_wrapper)
        return (request.json_parser(json_wrapper),limits)
    elif request.method == "PUT":
        response = requests.put(request.host + request.url, headers=request.header,timeout=(5,5))
        limits = get_limits_usage(response)
        json_wrapper = parse_json_from_string(response.text)
        print(response.text)
        check_response(json_wrapper)
        return (request.json_parser(json_wrapper),limits)


