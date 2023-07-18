class SymbolOrderBook:

    def __init__(self):
        self.symbol = ""
        self.bidPrice = 0.0
        self.bidQty = 0.0
        self.askPrice = 0.0
        self.askQty = 0.0

    @staticmethod
    def json_parse(json_data):
        result = SymbolOrderBook()
        result.symbol = json_data.get_string("symbol")
        result.bidPrice = json_data.get_float("bidPrice")
        result.bidQty = json_data.get_float("bidQty")
        result.askPrice = json_data.get_float("askPrice")
        result.askQty = json_data.get_float("askQty")
        return result