from binance_f.impl import RestApiRequest
from binance_f.impl.utils.urlparamsbuilder import UrlParamsBuilder
from binance_f.impl.utils.apisignature import create_signature
from binance_f.impl.utils.apisignature import create_signature_with_query
from binance_f.impl.utils.inputchecker import *
from binance_f.impl.utils.timeservice import *
from binance_f.model import *
# For develop
from binance_f.base.printobject import *


class RestApiRequestImpl(object):

    def __init__(self, api_key, secret_key, server_url="https://fapi.binance.com"):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__server_url = server_url

    def __create_request_by_get(self, url, builder):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        request.header.update({'Content-Type': 'application/json'})
        request.url = url + "?" + builder.build_url()
        return request

    def __create_request_by_get_with_apikey(self, url, builder):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        builder.put_url("recvWindow", 5000)
        builder.put_url("timestamp", str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url = url + "?" + builder.build_url()
        return request

    def __create_request_by_post_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        builder.put_url("recvWindow", 5000)
        builder.put_url("timestamp", str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.post_body = builder.post_map
        request.url = url + "?" + builder.build_url()
        return request

    def __create_request_by_delete_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = "DELETE"
        request.host = self.__server_url
        builder.put_url("recvWindow", 5000)
        builder.put_url("timestamp", str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url = url + "?" + builder.build_url()
        return request

    def __create_request_by_get_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        
        ts = str(get_current_timestamp() -1000)
        
        builder.put_url("recvWindow", 60000)
        builder.put_url("timestamp",ts)
        create_signature(self.__secret_key, builder)

        
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url = url + "?" + builder.build_url()
        return request

    def __create_request_by_put_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = "PUT"
        request.host = self.__server_url
        builder.put_url("recvWindow", 60000)
        builder.put_url("timestamp", str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url = url + "?" + builder.build_url()
        # For develop
        print("====== Request ======")
        print(request)
        PrintMix.print_data(request)
        print("=====================")
        return request
        
    def get_servertime(self):
        builder = UrlParamsBuilder()
        request = self.__create_request_by_get("/fapi/v1/time", builder)

        def parse(json_wrapper):
            result = json_wrapper.get_int("serverTime")
            return result

        request.json_parser = parse
        return request
         
    def get_exchange_information(self):
        builder = UrlParamsBuilder()
        request = self.__create_request_by_get("/fapi/v1/exchangeInfo", builder)

        def parse(json_wrapper):
            result = ExchangeInformation.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request
                
    def get_order_book(self, symbol, limit):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/depth", builder)

        def parse(json_wrapper):
            result = OrderBook.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request
       
    def get_recent_trades_list(self, symbol, limit):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/trades", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Trade.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
    
    def get_old_trade_lookup(self, symbol, limit, fromId):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("limit", limit)
        builder.put_url("fromId", fromId)

        request = self.__create_request_by_get_with_apikey("/fapi/v1/historicalTrades", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Trade.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
          
    def get_aggregate_trades_list(self, symbol, fromId, startTime, endTime, limit):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("fromId", fromId)
        builder.put_url("startTime", startTime)
        builder.put_url("endTime", endTime)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/aggTrades", builder)

        def parse(json_wrapper):
            aggregate_trades_list = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                trade = AggregateTrade.json_parse(item)
                aggregate_trades_list.append(trade)
            return aggregate_trades_list

        request.json_parser = parse
        return request
          
    def get_candlestick_data(self, symbol, interval, startTime, endTime, limit):
        check_should_not_none(symbol, "symbol")
        check_should_not_none(symbol, "interval")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("interval", interval)
        builder.put_url("startTime", startTime)
        builder.put_url("endTime", endTime)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/klines", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Candlestick.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_mark_price(self, symbol):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)

        request = self.__create_request_by_get("/fapi/v1/premiumIndex", builder)

        def parse(json_wrapper):
            result = MarkPrice.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_funding_rate(self, symbol, startTime, endTime, limit):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("startTime", startTime)
        builder.put_url("endTime", endTime)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/fundingRate", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = FundingRate.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
      
    def get_ticker_price_change_statistics(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)

        request = self.__create_request_by_get("/fapi/v1/ticker/24hr", builder)

        def parse(json_wrapper):
            result = list()

            if symbol:
                element = TickerPriceChangeStatistics.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = TickerPriceChangeStatistics.json_parse(item)
                    result.append(element)

            return result

        request.json_parser = parse
        return request

    def get_symbol_price_ticker(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)

        request = self.__create_request_by_get("/fapi/v1/ticker/price", builder)

        def parse(json_wrapper):
            result = list()
            if symbol:
                element = SymbolPrice.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = SymbolPrice.json_parse(item)
                    result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_symbol_orderbook_ticker(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)

        request = self.__create_request_by_get("/fapi/v1/ticker/bookTicker", builder)

        def parse(json_wrapper):
            result = list()
            if symbol:
                element = SymbolOrderBook.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = SymbolOrderBook.json_parse(item)
                    result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_open_interest(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)

        request = self.__create_request_by_get("/fapi/v1/openInterest", builder)

        def parse(json_wrapper):
            result = list()
            element = OpenInterest.json_parse(json_wrapper)
            result.append(element)
            return element

        request.json_parser = parse
        return request


    def get_liquidation_orders(self, symbol, startTime, endTime, limit):
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("startTime", startTime)
        builder.put_url("endTime", endTime)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get("/fapi/v1/allForceOrders", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = LiquidationOrder.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
     
   
    def change_position_mode(self, dualSidePosition):
        check_should_not_none(dualSidePosition, "dualSidePosition")
        builder = UrlParamsBuilder()
        builder.put_url("dualSidePosition", dualSidePosition)
        
        request = self.__create_request_by_post_with_signature("/fapi/v1/positionSide/dual", builder)

        def parse(json_wrapper):
            result = CodeMsg.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request


    def get_position_mode(self):
        
        request = self.__create_request_by_get_with_signature("/fapi/v1/positionSide/dual", builder)

        def parse(json_wrapper):
            result = PositionMode.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def cancel_all_orders(self, symbol):
        print(symbol)
        request = RestApiRequest()
        request.method = "DELETE"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/allOpenOrders?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def post_auto_order_with_price(self, symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        reduceOnlyStr = "true"
        if not reduceOnly:
            reduceOnlyStr = "false"
        extraUrl = "newClientOrderId="+newClientOrderId+"&price="+str(price)+"&symbol="+symbol+"&side="+side+"&type="+ordertype+"&timeInForce="+timeInForce+"&quantity="+str(quantity)+"&reduceOnly="+reduceOnlyStr+"&stopPrice="+str(stopPrice)+"&positionSide="+positionSide+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def post_auto_order(self, symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        reduceOnlyStr = "true"
        if not reduceOnly:
            reduceOnlyStr = "false"
        extraUrl = "newClientOrderId="+newClientOrderId+"&symbol="+symbol+"&side="+side+"&type="+ordertype+"&timeInForce="+timeInForce+"&quantity="+str(quantity)+"&reduceOnly="+reduceOnlyStr+"&stopPrice="+str(stopPrice)+"&positionSide="+positionSide+"&workingType=CONTRACT_PRICE&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
        
    def post_order(self, symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        reduceOnlyStr = "true"
        if not reduceOnly:
            reduceOnlyStr = "false"
        extraUrl = "newClientOrderId="+newClientOrderId+"&symbol="+symbol+"&side="+side+"&type="+ordertype+"&timeInForce="+timeInForce+"&quantity="+str(quantity)+"&reduceOnly="+reduceOnlyStr+"&price="+str(price)+"&positionSide="+positionSide+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def post_market_order(self, symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        reduceOnlyStr = "true"
        if not reduceOnly:
            reduceOnlyStr = "false"
        extraUrl = "symbol="+symbol+"&side="+side+"&type="+ordertype+"&quantity="+str(quantity)+"&reduceOnly="+reduceOnlyStr+"&positionSide="+positionSide+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_order(self, symbol, orderId, origClientOrderId):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("orderId", orderId)
        builder.put_url("origClientOrderId", origClientOrderId)

        request = self.__create_request_by_get_with_signature("/fapi/v1/order", builder)

        def parse(json_wrapper):
            result = Order.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_order_by_client_id(self, symbol, origClientOrderId):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&origClientOrderId="+origClientOrderId+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl


        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def cancel_order(self, symbol, origClientOrderId):
        request = RestApiRequest()
        request.method = "DELETE"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&origClientOrderId="+str(origClientOrderId)+"&timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl
        def parse(json_wrapper):
            result = Order.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def cancel_list_orders(self, symbol, orderIdList, origClientOrderIdList):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("orderIdList", orderIdList)
        builder.put_url("origClientOrderIdList", origClientOrderIdList)
        request = self.__create_request_by_delete_with_signature("/fapi/v1/batchOrders", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                if item.contain_key("code"):
                    element = Msg.json_parse(item)
                else:
                    element = Order.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_all_orders(self, symbol):
        # check_should_not_none(symbol, "symbol")
        # builder = UrlParamsBuilder()
        # builder.put_url("symbol", symbol)
        # builder.put_url("orderId", orderId)
        # builder.put_url("startTime", startTime)
        # builder.put_url("endTime", endTime)
        # builder.put_url("limit", limit)

        # request = self.__create_request_by_get_with_signature("/fapi/v1/allOrders", builder)

        # def parse(json_wrapper):
        #     result = list()
        #     data_list = json_wrapper.convert_2_array()
        #     for item in data_list.get_items():
        #         element = Order.json_parse(item)
        #         result.append(element)
        #     return result

        # request.json_parser = parse
        # return request
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&timestamp="+ts+"&recvWindow=60000&limit=1000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/allOrders?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_balance(self):
        # builder = UrlParamsBuilder()

        # request = self.__create_request_by_get_with_signature("/fapi/v1/balance", builder)

        # def parse(json_wrapper):
        #     result = list()
        #     data_list = json_wrapper.convert_2_array()
        #     for item in data_list.get_items():
        #         element = Balance.json_parse(item)
        #         result.append(element)
        #     return result

        # request.json_parser = parse
        # return request
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v2/balance?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_all_open_orders(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/openOrders?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_open_orders(self, symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl =  "symbol="+symbol+"&timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/openOrders?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_commission_rate(self, symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl =  "symbol="+symbol+"&timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/commissionRate?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_account_information(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v2/account?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
    
    def change_initial_leverage(self, symbol, leverage):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&leverage="+str(leverage)+"&recvWindow=60000&timestamp="+ts+""


        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/leverage?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def change_margin_type(self, symbol, marginType):
        check_should_not_none(symbol, "symbol")
        check_should_not_none(marginType, "marginType")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("marginType", marginType)

        request = self.__create_request_by_post_with_signature("/fapi/v1/marginType", builder)

        def parse(json_wrapper):
            result = CodeMsg.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request
    
    def change_position_margin(self, symbol, amount, type):
        check_should_not_none(symbol, "symbol")
        check_should_not_none(amount, "amount")
        check_should_not_none(type, "type")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("amount", amount)
        builder.put_url("type", type)

        request = self.__create_request_by_post_with_signature("/fapi/v1/positionMargin", builder)

        def parse(json_wrapper):
            result = PositionMargin.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_position_margin_change_history(self, symbol, type, startTime, endTime, limit):
        check_should_not_none(symbol, "symbol")
        builder = UrlParamsBuilder()
        builder.put_url("symbol", symbol)
        builder.put_url("type", type)
        builder.put_url("startTime", startTime)
        builder.put_url("endTime", endTime)
        builder.put_url("limit", limit)

        request = self.__create_request_by_get_with_signature("/fapi/v1/positionMargin/history", builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = PositionMarginHist.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_position_with_symbol(self,symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v2/positionRisk?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_position(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v2/positionRisk?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_account_risk(self,symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&timestamp="+ts+"&recvWindow=60000"

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v2/positionRisk?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_account_trades_with_ts(self, symbol,limit,startTime,endTime):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&limit="+str(limit)+"&recvWindow=60000&timestamp="+ts+"&startTime="+str(startTime)+"&endTime="+str(endTime)+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/userTrades?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_account_trades_with_from_id(self, symbol,limit):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&limit="+str(limit)+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/userTrades?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_account_trades(self, symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&limit=100&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/userTrades?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_income_history(self, symbol):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&limit=1000&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/income?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_income_history_with_no_symbol(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "limit=1000&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/income?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_income_history_with_start_time(self,startTime):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "limit=1000&recvWindow=60000&timestamp="+ts+"&startTime="+str(startTime)+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/income?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_fee_history(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "incomeType=COMMISSION&limit=1000&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/income?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def start_user_data_stream(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_post_with_signature("/fapi/v1/listenKey", builder)

        def parse(json_wrapper):
            result = json_wrapper.get_string("listenKey")
            return result

        request.json_parser = parse
        return request
      
    def keep_user_data_stream(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_put_with_signature("/fapi/v1/listenKey", builder)

        def parse(json_wrapper):
            result = "OK"
            return result

        request.json_parser = parse
        return request
      
    def close_user_data_stream(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_delete_with_signature("/fapi/v1/listenKey", builder)

        def parse(json_wrapper):
            result = "OK"
            return result

        request.json_parser = parse
        return request
      

    def query_order(self,symbol,orderID):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&orderID="+str(orderID)+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def query_order_with_client_order_id(self,symbol,orderID):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "symbol="+symbol+"&origClientOrderId="+str(orderID)+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/order?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def batch_orders(self,batchOrders):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "batchOrders="+batchOrders+"&recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/batchOrders?" + extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def get_listen_key(self):
        request = RestApiRequest()
        request.method = "POST"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = ""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/listenKey" 

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request


    def extend_listen_key(self):
        request = RestApiRequest()
        request.method = "PUT"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = ""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/listenKey" 

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_api_trading_status(self):
        request = RestApiRequest()
        request.method = "GET"
        request.host = self.__server_url
        ts = str(get_current_timestamp() -1000)
        extraUrl = "recvWindow=60000&timestamp="+ts+""

        sign=create_signature(self.__secret_key, extraUrl)
        extraUrl = extraUrl+"&signature="+sign
        request.header.update({"Content-Type": "application/x-www-form-urlencoded"})
        request.header.update({"X-MBX-APIKEY": self.__api_key})
        request.url =  "/fapi/v1/apiTradingStatus?"+extraUrl

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Position.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request
