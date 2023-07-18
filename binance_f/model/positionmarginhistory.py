class PositionMarginHist:

    def __init__(self):
        self.amount = 0.0
        self.asset = ""
        self.symbol = ""
        self.time = 0
        self.type = 0

    @staticmethod
    def json_parse(json_data):
        result = PositionMarginHist()
        result.amount = json_data.get_float("amount")
        result.asset = json_data.get_string("asset")
        result.symbol = json_data.get_string("symbol")
        result.time = json_data.get_int("time")
        result.type = json_data.get_int("type")

        return result
