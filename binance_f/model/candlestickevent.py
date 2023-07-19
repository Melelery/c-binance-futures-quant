class Candlestick:

    def __init__(self):
        self.startTime = 0
        self.closeTime = 0
        self.symbol = ""
        self.interval = ""
        self.firstTradeId = 0
        self.lastTradeId = 0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.volume = 0.0
        self.numTrades = 0
        self.isClosed = False
        self.quoteAssetVolume = 0.0
        self.takerBuyBaseAssetVolume = 0.0
        self.takerBuyQuoteAssetVolume = 0.0
        self.ignore = 0.0

    @staticmethod
    def json_parse(json_data):
        data_obj = Candlestick()
        data_obj.startTime = json_data.get_int("t")
        data_obj.closeTime = json_data.get_int("T")
        data_obj.symbol = json_data.get_string("s")
        data_obj.interval = json_data.get_string("i")
        data_obj.firstTradeId = json_data.get_int("f")
        data_obj.lastTradeId = json_data.get_int("L")
        data_obj.open = json_data.get_float("o")
        data_obj.close = json_data.get_float("c")
        data_obj.high = json_data.get_float("h")
        data_obj.low = json_data.get_float("l")
        data_obj.volume = json_data.get_float("v")
        data_obj.numTrades = json_data.get_int("n")
        data_obj.isClosed = json_data.get_boolean("x")
        data_obj.quoteAssetVolume = json_data.get_float("q")
        data_obj.takerBuyBaseAssetVolume = json_data.get_float("V")
        data_obj.takerBuyQuoteAssetVolume = json_data.get_float("Q")
        data_obj.ignore = json_data.get_int("B")
  
        return data_obj


class CandlestickEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.data = Candlestick()

    @staticmethod
    def json_parse(json_wrapper):
        candlestick_event = CandlestickEvent()
        candlestick_event.eventType = json_wrapper.get_string("e")
        candlestick_event.eventTime = json_wrapper.get_int("E")
        candlestick_event.symbol = json_wrapper.get_string("s")
        data = Candlestick.json_parse(json_wrapper.get_object("k"))
        candlestick_event.data = data
        return candlestick_event

