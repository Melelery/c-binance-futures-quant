

class OpenInterest:

    def __init__(self):
        self.symbol = ""
        self.openInterest = 0.0
    
    @staticmethod
    def json_parse(json_data):
        result = OpenInterest()
        result.symbol = json_data.get_string("symbol")
        result.openInterest = json_data.get_float("openInterest")

        return result
