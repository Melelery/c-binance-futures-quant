class SymbolBookTickerEvent:

    def __init__(self):
        self.orderBookUpdateId = None
        self.symbol = ""
        self.bestBidPrice = 0.0
        self.bestBidQty = 0.0
        self.bestAskPrice = 0.0
        self.bestAskQty = 0.0

    @staticmethod
    def json_parse(json_wrapper):
        ticker_event = SymbolBookTickerEvent()
        ticker_event.orderBookUpdateId = json_wrapper.get_int("u")
        ticker_event.symbol = json_wrapper.get_string("s")
        ticker_event.bestBidPrice = json_wrapper.get_float("b")
        ticker_event.bestBidQty = json_wrapper.get_float("B")
        ticker_event.bestAskPrice = json_wrapper.get_float("a")
        ticker_event.bestAskQty = json_wrapper.get_float("A")
        return ticker_event