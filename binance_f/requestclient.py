from binance_f.constant.system import RestApiDefine
from binance_f.impl.restapirequestimpl import RestApiRequestImpl
from binance_f.impl.restapiinvoker import call_sync
from binance_f.model.constant import *


class RequestClient(object):

    def __init__(self, **kwargs):
        """
        Create the request client instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from Binance.
            secret_key: The private key applied from Binance.
            server_url: The URL name like "https://api.binance.com".
        """
        api_key = None
        secret_key = None
        url = RestApiDefine.Url
        if "api_key" in kwargs:
            api_key = kwargs["api_key"]
        if "secret_key" in kwargs:
            secret_key = kwargs["secret_key"]
        if "url" in kwargs:
            url = kwargs["url"]
        try:
            self.request_impl = RestApiRequestImpl(api_key, secret_key, url)
        except Exception:
            pass
        self.limits = {}
    
    def refresh_limits(self,limits):
        for k,v in limits.items():
            self.limits[k] = v

    def get_servertime(self) -> any:
        """
        Check Server Time

        GET /fapi/v1/time

        Test connectivity to the Rest API and get the current server time.
        """
        response = call_sync(self.request_impl.get_servertime())
        self.refresh_limits(response[1])
        return response[0]
               
    def get_exchange_information(self) -> any:
        """
        Exchange Information (MARKET_DATA)

        GET /fapi/v1/exchangeInfo

        Current exchange trading rules and symbol information
        """
        response = call_sync(self.request_impl.get_exchange_information())
        self.refresh_limits(response[1])
        return response[0]

    def get_order_book(self, symbol: 'str', limit: 'int' = None) -> any:
        """
        Order Book (MARKET_DATA)

        GET /fapi/v1/depth

        Adjusted based on the limit:
        """
        response = call_sync(self.request_impl.get_order_book(symbol, limit))
        # self.refresh_limits(response[1])
        return response
           
    def get_recent_trades_list(self, symbol: 'str', limit: 'int' = None) -> any:
        """
        Recent Trades List (MARKET_DATA)

        GET /fapi/v1/trades

        Get recent trades (up to last 500).
        """
        response = call_sync(self.request_impl.get_recent_trades_list(symbol, limit))
        self.refresh_limits(response[1])
        return response[0]
           
    def get_old_trade_lookup(self, symbol: 'str', limit: 'int' = None, fromId: 'long' = None) -> any:
        """
        Old Trades Lookup (MARKET_DATA)

        GET /fapi/v1/historicalTrades

        Get older market historical trades.
        """
        response = call_sync(self.request_impl.get_old_trade_lookup(symbol, limit, fromId))
        self.refresh_limits(response[1])
        return response[0]
            
    def get_aggregate_trades_list(self, symbol: 'str', fromId: 'long' = None, 
                            startTime: 'long' = None, endTime: 'long' = None, limit: 'int' = None) -> any:
        """
        Compressed/Aggregate Trades List (MARKET_DATA)

        GET /fapi/v1/aggTrades

        Get compressed, aggregate trades. Trades that fill at the time, from the same order, 
        with the same price will have the quantity aggregated.
        """
        response = call_sync(self.request_impl.get_aggregate_trades_list(symbol, fromId, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]
              
    def get_candlestick_data(self, symbol: 'str', interval: 'CandlestickInterval', 
                            startTime: 'long' = None, endTime: 'long' = None, limit: 'int' = None) -> any:
        """
        Kline/Candlestick Data (MARKET_DATA)

        GET /fapi/v1/klines

        Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
        """
        response = call_sync(self.request_impl.get_candlestick_data(symbol, interval, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]
            
    def get_mark_price(self, symbol: 'str') -> any:
        """
        Mark Price (MARKET_DATA)

        GET /fapi/v1/premiumIndex

        Mark Price and Funding Rate
        """
        response = call_sync(self.request_impl.get_mark_price(symbol))
        self.refresh_limits(response[1])
        return response[0]
            
    def get_funding_rate(self, symbol: 'str', startTime: 'long' = None, endTime: 'str' = None, limit: 'int' = None) -> any:
        """
        Get Funding Rate History (MARKET_DATA)

        GET /fapi/v1/fundingRate
        """
        response = call_sync(self.request_impl.get_funding_rate(symbol, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]
       
    def get_ticker_price_change_statistics(self, symbol: 'str' = None) -> any:
        """
        24hr Ticker Price Change Statistics (MARKET_DATA)

        GET /fapi/v1/ticker/24hr

        24 hour rolling window price change statistics.
        Careful when accessing this with no symbol.
        """
        response = call_sync(self.request_impl.get_ticker_price_change_statistics(symbol))
        self.refresh_limits(response[1])
        return response[0]
               
    def get_symbol_price_ticker(self, symbol: 'str' = None) -> any:
        """
        Symbol Price Ticker (MARKET_DATA)

        GET /fapi/v1/ticker/price

        Latest price for a symbol or symbols.
        """
        response = call_sync(self.request_impl.get_symbol_price_ticker(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_symbol_orderbook_ticker(self, symbol: 'str' = None) -> any:
        """
        Symbol Order Book Ticker (MARKET_DATA)

        GET /fapi/v1/ticker/bookTicker

        Best price/qty on the order book for a symbol or symbols.
        """
        response = call_sync(self.request_impl.get_symbol_orderbook_ticker(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_liquidation_orders(self, symbol: 'str' = None, startTime: 'long' = None, endTime: 'str' = None, 
                                limit: 'int' = None) -> any:
        """
        Get all Liquidation Orders (MARKET_DATA)

        GET /fapi/v1/allForceOrders
        """
        response = call_sync(self.request_impl.get_liquidation_orders(symbol, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]
   
    def get_open_interest(self, symbol: 'str') -> any:
        """
        Symbol Open Interest (MARKET_DATA)

        GET /fapi/v1/openInterest

        Get present open interest of a specific symbol.
        """
        response = call_sync(self.request_impl.get_open_interest(symbol))
        self.refresh_limits(response[1])
        return response[0]


    def change_position_mode(self, dualSidePosition: 'boolean' = None) -> any:
        """
        Change Current Position Mode (TRADE)

        POST /fapi/v1/positionSide/dual (HMAC SHA256)

        Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol
        """
        response = call_sync(self.request_impl.change_position_mode(dualSidePosition))
        self.refresh_limits(response[1])
        return response[0]


    def get_position_mode(self) -> any:
        """
        Get Current Position Mode (USER_DATA)

        GET /fapi/v1/positionSide/dual (HMAC SHA256)

        Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol
        """
        response = call_sync(self.request_impl.get_position_mode())
        self.refresh_limits(response[1])
        return response[0]
    def post_market_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType',
                timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                reduceOnly: 'boolean' = None, price: 'float' = None,
                newClientOrderId: 'str' = None, stopPrice: 'float' = None,
                workingType: 'WorkingType' = WorkingType.INVALID, closePosition: 'boolean' = None,
                positionSide: 'PositionSide' = PositionSide.INVALID, callbackRate: 'float' = None,
                activationPrice: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:
        """
        New Order (TRADE)

        POST /fapi/v1/order (HMAC SHA256)

        Send in a new order.
        """
        response = call_sync(self.request_impl.post_market_order(symbol, side, ordertype,
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType))

        return response

    def post_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType', 
                timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                reduceOnly: 'boolean' = None, price: 'float' = None,
                newClientOrderId: 'str' = None, stopPrice: 'float' = None, 
                workingType: 'WorkingType' = WorkingType.INVALID, closePosition: 'boolean' = None,
                positionSide: 'PositionSide' = PositionSide.INVALID, callbackRate: 'float' = None,
                activationPrice: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:
        """
        New Order (TRADE)

        POST /fapi/v1/order (HMAC SHA256)

        Send in a new order.
        """
        response = call_sync(self.request_impl.post_order(symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType))

        return response

    def post_auto_order_with_price(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType', 
                timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                reduceOnly: 'boolean' = None, price: 'float' = None,
                newClientOrderId: 'str' = None, stopPrice: 'float' = None, 
                workingType: 'WorkingType' = WorkingType.INVALID, closePosition: 'boolean' = None,
                positionSide: 'PositionSide' = PositionSide.INVALID, callbackRate: 'float' = None,
                activationPrice: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:
        """
        New Order (TRADE)

        POST /fapi/v1/order (HMAC SHA256)

        Send in a new order.
        """
        response = call_sync(self.request_impl.post_auto_order_with_price(symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType))

        return response

    def post_auto_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType', 
                timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                reduceOnly: 'boolean' = None, price: 'float' = None,
                newClientOrderId: 'str' = None, stopPrice: 'float' = None, 
                workingType: 'WorkingType' = WorkingType.INVALID, closePosition: 'boolean' = None,
                positionSide: 'PositionSide' = PositionSide.INVALID, callbackRate: 'float' = None,
                activationPrice: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:
        """
        New Order (TRADE)

        POST /fapi/v1/order (HMAC SHA256)

        Send in a new order.
        """
        response = call_sync(self.request_impl.post_auto_order(symbol, side, ordertype, 
                timeInForce, quantity, reduceOnly, price, newClientOrderId, stopPrice, workingType, closePosition, positionSide, callbackRate, activationPrice, newOrderRespType))

        return response

    def cancel_all_orders(self, symbol: 'str') -> any:
        """
        Cancel All Open Orders (TRADE)

        DELETE /fapi/v1/allOpenOrders (HMAC SHA256)
        """
        response = call_sync(self.request_impl.cancel_all_orders(symbol))
        return response


    def get_order(self, symbol: 'str', orderId: 'long' = None, origClientOrderId: 'str' = None) -> any:
        """
        Query Order (USER_DATA)

        GET /fapi/v1/order (HMAC SHA256)

        Check an order's status.
        """
        response = call_sync(self.request_impl.get_order(symbol, orderId, origClientOrderId))
        self.refresh_limits(response[1])
        return response[0]

    def get_order_by_client_id(self, symbol: 'str', origClientOrderId: 'str') -> any:
        """
        Cancel Order (TRADE)

        DELETE /fapi/v1/order (HMAC SHA256)

        Cancel an active order.
        """
        response = call_sync(self.request_impl.get_order_by_client_id(symbol,origClientOrderId))
        return response

  
    def cancel_order(self, symbol: 'str', orderId: 'long') -> any:
        """
        Cancel Order (TRADE)

        DELETE /fapi/v1/order (HMAC SHA256)

        Cancel an active order.
        """
        response = call_sync(self.request_impl.cancel_order(symbol,orderId))
        return response




    def cancel_list_orders(self, symbol: 'str', orderIdList: 'list' = None, origClientOrderIdList: 'list' = None) -> any:
        """
        Cancel Multiple Orders (TRADE)

        DELETE /fapi/v1/batchOrders (HMAC SHA256)
        """
        response = call_sync(self.request_impl.cancel_list_orders(symbol, orderIdList, origClientOrderIdList))
        self.refresh_limits(response[1])
        return response[0]

    def get_open_orders(self, symbol: 'str' = None) -> any:
        """
        Current Open Orders (USER_DATA)

        GET /fapi/v1/openOrders (HMAC SHA256)

        Get all open orders on a symbol. Careful when accessing this with no symbol.
        """
        response = call_sync(self.request_impl.get_open_orders(symbol))
        return response


    def get_commission_rate(self, symbol: 'str' = None) -> any:
        """
        Current Open Orders (USER_DATA)

        GET /fapi/v1/openOrders (HMAC SHA256)

        Get all open orders on a symbol. Careful when accessing this with no symbol.
        """
        response = call_sync(self.request_impl.get_commission_rate(symbol))
        return response

    def get_all_open_orders(self) -> any:
        """
        Current Open Orders (USER_DATA)

        GET /fapi/v1/openOrders (HMAC SHA256)

        Get all open orders on a symbol. Careful when accessing this with no symbol.
        """
        response = call_sync(self.request_impl.get_all_open_orders())
        return response

    def get_all_orders(self, symbol: 'str', orderId: 'long' = None, startTime: 'long' = None, 
                        endTime: 'long' = None, limit: 'int' = None) -> any:
        """
        All Orders (USER_DATA)

        GET /fapi/v1/allOrders (HMAC SHA256)

        Get all account orders; active, canceled, or filled.
        """
        response = call_sync(self.request_impl.get_all_orders(symbol))
        return response

    def get_balance(self) -> any:
        """
        Future Account Balance (USER_DATA)

        Get /fapi/v1/balance (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_balance())
        return response
        # response = call_sync(self.request_impl.get_balance())
        # self.refresh_limits(response[1])
        # return response[0]

    def get_account_information(self) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.get_account_information())
        return response

    def change_initial_leverage(self, symbol, leverage) -> any:
        """
        Change Initial Leverage (TRADE)

        POST /fapi/v1/leverage (HMAC SHA256)

        Change user's initial leverage of specific symbol market.
        """
        response = call_sync(self.request_impl.change_initial_leverage(symbol, leverage))
        return response

    def change_margin_type(self, symbol: 'str', marginType: 'FuturesMarginType') -> any:
        """
        Change Margin Type (TRADE)

        POST /fapi/v1/marginType (HMAC SHA256)
        """
        response = call_sync(self.request_impl.change_margin_type(symbol, marginType))
        self.refresh_limits(response[1])
        return response[0]

    def change_position_margin(self, symbol: 'str', amount: 'float', type: 'int') -> any:
        """
        Modify Isolated Position Margin (TRADE)

        POST /fapi/v1/positionMargin (HMAC SHA256)
        """
        response = call_sync(self.request_impl.change_position_margin(symbol, amount, type))
        self.refresh_limits(response[1])
        return response[0]

    def get_position_margin_change_history(self, symbol: 'str', type: 'int' = None, startTime: 'int' = None, endTime: 'int' = None, limit :'int' = None) -> any:
        """
        Get Position Margin Change History (TRADE)

        GET /fapi/v1/positionMargin/history (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_position_margin_change_history(symbol, type, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_account_risk(self,symbol) -> any:
        """
        Position Information (USER_DATA)

        GET /dapi/v1/positionRisk (HMAC SHA256) Get current account information.
        """
        response = call_sync(self.request_impl.get_account_risk(symbol))
        return response

    def get_position_with_symbol(self,symbol) -> any:
        """
        Position Information (USER_DATA)

        GET /fapi/v1/positionRisk (HMAC SHA256) Get current account information.
        """
        response = call_sync(self.request_impl.get_position_with_symbol(symbol))
        return response

    def get_position(self) -> any:
        """
        Position Information (USER_DATA)

        GET /fapi/v1/positionRisk (HMAC SHA256) Get current account information.
        """
        response = call_sync(self.request_impl.get_position())
        return response

    def get_account_trades_with_ts(self,symbol,limit,startTime,endTime) -> any:
        """
        Account Trade List (USER_DATA)

        GET /dapi/v1/userTrades (HMAC SHA256)

        Get trades for a specific account and symbol.
        """
        response = call_sync(self.request_impl.get_account_trades_with_ts(symbol,limit,startTime,endTime))
        return response

    def get_account_trades_with_from_id(self,symbol,limit) -> any:
        """
        Account Trade List (USER_DATA)

        GET /dapi/v1/userTrades (HMAC SHA256)

        Get trades for a specific account and symbol.
        """
        response = call_sync(self.request_impl.get_account_trades_with_from_id(symbol,limit))
        return response

    def get_account_trades(self,symbol) -> any:
        """
        Account Trade List (USER_DATA)

        GET /dapi/v1/userTrades (HMAC SHA256)

        Get trades for a specific account and symbol.
        """
        response = call_sync(self.request_impl.get_account_trades(symbol))
        return response

    def get_income_history(self,symbol) -> any:
        """
        Get Income History(USER_DATA)

        GET /dapi/v1/income (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_income_history(symbol))
        return response

    def get_income_history_with_no_symbol(self) -> any:
        """
        Get Income History(USER_DATA)

        GET /dapi/v1/income (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_income_history_with_no_symbol())
        return response

    def get_income_history_with_start_time(self,startTime) -> any:
        """
        Get Income History(USER_DATA)

        GET /dapi/v1/income (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_income_history_with_start_time(startTime))
        return response


    def get_fee_history(self) -> any:
        """
        Get Income History(USER_DATA)

        GET /dapi/v1/income (HMAC SHA256)
        """
        response = call_sync(self.request_impl.get_fee_history())
        return response


    def start_user_data_stream(self) -> any:
        """
        Start User Data Stream (USER_STREAM)

        POST /fapi/v1/listenKey (HMAC SHA256)

        Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent. 
        If the account has an active listenKey, 
        that listenKey will be returned and its validity will be extended for 60 minutes.
        """
        response = call_sync(self.request_impl.start_user_data_stream())
        self.refresh_limits(response[1])
        return response[0]

    def keep_user_data_stream(self) -> any:
        """
        Keepalive User Data Stream (USER_STREAM)

        PUT /fapi/v1/listenKey (HMAC SHA256)

        Keepalive a user data stream to prevent a time out. User data streams will close after 60 minutes. 
        It's recommended to send a ping about every 60 minutes.
        """
        response = call_sync(self.request_impl.keep_user_data_stream())
        self.refresh_limits(response[1])
        return response[0]

    def close_user_data_stream(self) -> any:
        """
        Close User Data Stream (USER_STREAM)

        DELETE /fapi/v1/listenKey (HMAC SHA256)

        Close out a user data stream.
        """
        response = call_sync(self.request_impl.close_user_data_stream())
        self.refresh_limits(response[1])
        return response[0]

    def query_order(self,symbol,orderID) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.query_order(symbol,orderID))
        return response

    def query_order_with_client_order_id(self,symbol,orderID) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.query_order_with_client_order_id(symbol,orderID))
        return response

    def batch_orders(self,batchOrders) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.batch_orders(batchOrders))
        return response

    def get_listen_key(self) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.get_listen_key())
        return response

    def extend_listen_key(self) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.extend_listen_key())
        return response

    def get_api_trading_status(self) -> any:
        """
        Account Information (USER_DATA)

        GET /dapi/v1/account (HMAC SHA256)

        Get current account information.
        """
        response = call_sync(self.request_impl.get_api_trading_status())
        return response