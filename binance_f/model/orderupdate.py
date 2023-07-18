class OrderUpdate:
    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.transactionTime = 0
        self.symbol = ""
        self.clientOrderId = ""
        self.side = None
        self.type = None
        self.timeInForce = None
        self.origQty = 0.0
        self.price = 0.0
        self.avgPrice = 0.0
        self.stopPrice = 0.0
        self.executionType = ""
        self.orderStatus = ""
        self.orderId = None
        self.lastFilledQty = 0.0
        self.cumulativeFilledQty = 0.0
        self.lastFilledPrice = 0.0
        self.commissionAsset = None
        self.commissionAmount = 0
        self.orderTradeTime = 0
        self.tradeID = None
        self.bidsNotional = 0.0
        self.asksNotional = 0.0
        self.isMarkerSide = None
        self.isReduceOnly = None
        self.workingType = 0.0
        self.isClosePosition = None
        self.activationPrice = 0.0
        self.callbackRate = 0.0
        self.positionSide = None


    @staticmethod
    def json_parse(json_data):
        result = OrderUpdate()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.transactionTime = json_data.get_int("T")

        data_group = json_data.get_object("o")
        result.symbol = data_group.get_string("s")
        result.clientOrderId = data_group.get_string("c")
        result.side = data_group.get_string("S")
        result.type = data_group.get_string("o")
        result.timeInForce = data_group.get_string("f")
        result.origQty = data_group.get_float("q")
        result.price = data_group.get_float("p")
        result.avgPrice = data_group.get_float("ap")
        result.stopPrice = data_group.get_float("sp")
        result.executionType = data_group.get_string("x")
        result.orderStatus = data_group.get_string("X")
        result.orderId = data_group.get_int("i")
        result.lastFilledQty = data_group.get_float("l")
        result.cumulativeFilledQty = data_group.get_float("z")
        result.lastFilledPrice = data_group.get_float("L")
        result.commissionAsset = data_group.get_string_or_default("N", None)
        result.commissionAmount = data_group.get_float_or_default("n", None)
        result.orderTradeTime = data_group.get_int("T")
        result.tradeID = data_group.get_int("t")
        result.bidsNotional = data_group.get_float("b")
        result.asksNotional = data_group.get_float("a")
        result.isMarkerSide = data_group.get_boolean("m")
        result.isReduceOnly = data_group.get_boolean("R")
        result.workingType = data_group.get_string("wt")
        result.isClosePosition = data_group.get_boolean("cp")
        result.activationPrice = data_group.get_float_or_default("AP", None)
        result.callbackRate = data_group.get_float_or_default("cr", None)
        result.positionSide = data_group.get_string("ps")

        return result
