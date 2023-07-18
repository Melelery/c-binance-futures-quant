class Order:

    def __init__(self):
        self.clientOrderId = ""
        self.cumQuote = 0.0
        self.executedQty = None
        self.orderId = None
        self.origQty = None
        self.price = None
        self.reduceOnly = False
        self.side = None
        self.status = None
        self.stopPrice = None
        self.symbol = ""
        self.timeInForce = None
        self.type = None
        self.updateTime = 0
        self.workingType = ""
        self.avgPrice = 0.0
        self.origType = ""
        self.positionSide = ""
        self.activatePrice = None
        self.priceRate = None
        self.closePosition = None

    @staticmethod
    def json_parse(json_data):
        result = Order()
        result.clientOrderId = json_data.get_string("clientOrderId")
        result.cumQuote = json_data.get_float("cumQuote")
        result.executedQty = json_data.get_float_or_default("executedQty", None)
        result.orderId = json_data.get_int("orderId")
        result.origQty = json_data.get_float("origQty")
        result.price = json_data.get_float("price")
        result.reduceOnly = json_data.get_boolean("reduceOnly")
        result.side = json_data.get_string("side")
        result.status = json_data.get_string("status")
        result.stopPrice = json_data.get_float("stopPrice")
        result.symbol = json_data.get_string("symbol")
        result.timeInForce = json_data.get_string("timeInForce")
        result.type = json_data.get_string("type")
        result.updateTime = json_data.get_int("updateTime")
        result.workingType = json_data.get_string("workingType")
        result.avgPrice = json_data.get_float("avgPrice")
        result.origType = json_data.get_string("origType")
        result.positionSide = json_data.get_string("positionSide")
        result.activatePrice = json_data.get_float_or_default("activatePrice", None)
        result.priceRate = json_data.get_float_or_default("priceRate", None)
        result.closePosition = json_data.get_boolean("closePosition")

        return result
