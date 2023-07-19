class LiquidationOrder:

    def __init__(self):
        self.symbol = ""
        self.price = 0.0
        self.origQty = 0.0
        self.executedQty = 0.0
        self.averagePrice = 0.0
        self.timeInForce = ""
        self.type = ""
        self.side = ""
        self.time = 0
    
    @staticmethod
    def json_parse(json_data):
        result = LiquidationOrder()
        result.symbol = json_data.get_string("symbol")
        result.price = json_data.get_float("price")
        result.origQty = json_data.get_float("origQty")
        result.executedQty = json_data.get_float("executedQty")
        result.averagePrice = json_data.get_float("averagePrice")
        result.timeInForce = json_data.get_string("timeInForce")
        result.type = json_data.get_string("symbol")
        result.side = json_data.get_string("side")
        result.time = json_data.get_int("time")

        return result
