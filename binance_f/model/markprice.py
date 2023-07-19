

class MarkPrice:

    def __init__(self):
        self.symbol = ""
        self.markPrice = 0.0
        self.lastFundingRate = 0.0
        self.nextFundingTime = 0
        self.time = 0
    
    @staticmethod
    def json_parse(json_data):
        result = MarkPrice()
        result.symbol = json_data.get_string("symbol")
        result.markPrice = json_data.get_float("markPrice")
        result.lastFundingRate = json_data.get_float("lastFundingRate")
        result.nextFundingTime = json_data.get_int("nextFundingTime")
        result.time = json_data.get_int("time")

        return result
