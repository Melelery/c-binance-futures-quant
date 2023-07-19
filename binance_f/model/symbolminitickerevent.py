class SymbolMiniTickerEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.totalTradedBaseAssetVolume = 0.0
        self.totalTradedQuoteAssetVolume = 0.0

    @staticmethod
    def json_parse(json_wrapper):
        result = SymbolMiniTickerEvent()
        result.eventType = json_wrapper.get_string("e")
        result.eventTime = json_wrapper.get_int("E")
        result.symbol = json_wrapper.get_string("s")
        result.open = json_wrapper.get_float("o")
        result.close = json_wrapper.get_float("c")
        result.high = json_wrapper.get_float("h")
        result.low = json_wrapper.get_float("l")
        result.totalTradedBaseAssetVolume = json_wrapper.get_float("v")
        result.totalTradedQuoteAssetVolume = json_wrapper.get_float("q")
        return result