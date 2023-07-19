import base64
import hashlib
import hmac
import datetime
from urllib import parse
import urllib.parse
from binance_f.exception.binanceapiexception import BinanceApiException


def create_signature(secret_key, extraUrl):
    if secret_key is None or secret_key == "":
        raise BinanceApiException(BinanceApiException.KEY_MISSING,  "Secret key are required")
    signature = hmac.new(secret_key.encode(), msg=extraUrl.encode(), digestmod=hashlib.sha256).hexdigest()
    return signature


def create_signature_with_query(secret_key, query):
    if secret_key is None or secret_key == "":
        raise BinanceApiException(BinanceApiException.KEY_MISSING,  "Secret key are required")

    signature = hmac.new(secret_key.encode(), msg=query.encode(), digestmod=hashlib.sha256).hexdigest()
    
    return signature


def utc_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
