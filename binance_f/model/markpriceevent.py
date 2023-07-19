class MarkPriceEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.symbol = ""
        self.markPrice = 0.0
        self.fundingRate = 0.0
        self.nextFundingTime = 0

    @staticmethod
    def json_parse(json_data):
        result = MarkPriceEvent()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.symbol = json_data.get_string("s")
        result.markPrice = json_data.get_float("p")
        result.fundingRate = json_data.get_float("r")
        result.nextFundingTime = json_data.get_int("T")
        return result
