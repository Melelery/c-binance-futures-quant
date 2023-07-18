class SymbolTickerEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.priceChange = 0.0
        self.priceChangePercent = 0.0
        self.weightedAvgPrice = 0.0
        self.lastPrice = 0.0
        self.lastQty = 0.0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.totalTradedBaseAssetVolume = 0.0
        self.totalTradedQuoteAssetVolume = 0.0
        self.openTime = 0
        self.closeTime = 0
        self.firstId = None
        self.lastId = None
        self.count = 0

    @staticmethod
    def json_parse(json_wrapper):
        ticker_event = SymbolTickerEvent()
        ticker_event.eventType = json_wrapper.get_string("e")
        ticker_event.eventTime = json_wrapper.get_int("E")
        ticker_event.symbol = json_wrapper.get_string("s")
        ticker_event.priceChange = json_wrapper.get_float("p")
        ticker_event.priceChangePercent = json_wrapper.get_float("P")
        ticker_event.weightedAvgPrice = json_wrapper.get_float("w")
        ticker_event.lastPrice = json_wrapper.get_float("c")
        ticker_event.lastQty = json_wrapper.get_float("Q")
        ticker_event.open = json_wrapper.get_float("o")
        ticker_event.high = json_wrapper.get_float("h")
        ticker_event.low = json_wrapper.get_float("l")
        ticker_event.totalTradedBaseAssetVolume = json_wrapper.get_float("v")
        ticker_event.totalTradedQuoteAssetVolume = json_wrapper.get_float("q")
        ticker_event.openTime = json_wrapper.get_int("O")
        ticker_event.closeTime = json_wrapper.get_int("C")
        ticker_event.firstId = json_wrapper.get_int("F")
        ticker_event.lastId = json_wrapper.get_int("L")
        ticker_event.count = json_wrapper.get_int("n")
        return ticker_event