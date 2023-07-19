class FundingRate:

    def __init__(self):
        self.symbol = ""
        self.fundingRate = 0.0
        self.fundingTime = 0
    
    @staticmethod
    def json_parse(json_data):
        result = FundingRate()
        result.symbol = json_data.get_string("symbol")
        result.fundingRate = json_data.get_float("fundingRate")
        result.fundingTime = json_data.get_int("fundingTime")

        return result
