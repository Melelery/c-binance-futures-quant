class TickerPriceChangeStatistics:

    def __init__(self):
        self.symbol = ""
        self.priceChange = 0.0
        self.priceChangePercent = 0.0
        self.weightedAvgPrice = 0.0
        self.lastPrice = 0.0
        self.lastQty = 0.0
        self.bidPrice = 0.0
        self.askPrice = 0.0
        self.openPrice = 0.0
        self.highPrice = 0.0
        self.lowPrice = 0.0
        self.volume = 0.0
        self.quoteVolume = 0.0
        self.openTime = 0
        self.closeTime = 0
        self.firstId = None
        self.lastId = None
        self.count = None

    @staticmethod
    def json_parse(json_data):
        result = TickerPriceChangeStatistics()
        result.symbol = json_data.get_string("symbol")
        result.priceChange = json_data.get_float("priceChange")
        result.priceChangePercent = json_data.get_float("priceChangePercent")
        result.weightedAvgPrice = json_data.get_float("weightedAvgPrice")
        result.lastPrice = json_data.get_float("lastPrice")
        result.lastQty = json_data.get_float("lastQty")
        result.openPrice = json_data.get_float("openPrice")
        result.highPrice = json_data.get_float("highPrice")
        result.lowPrice = json_data.get_float("lowPrice")
        result.volume = json_data.get_float("volume")
        result.quoteVolume = json_data.get_float("quoteVolume")
        result.openTime = json_data.get_int("openTime")
        result.closeTime = json_data.get_int("closeTime")
        result.firstId = json_data.get_int("firstId")
        result.lastId = json_data.get_int("lastId")
        result.count = json_data.get_int("count")
        return result