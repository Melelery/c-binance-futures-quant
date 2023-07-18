class PositionMargin:

    def __init__(self):
        self.code = 0
        self.msg = ""
        self.amount = 0.0
        self.type = 0

    @staticmethod
    def json_parse(json_data):
        result = PositionMargin()
        result.code = json_data.get_int("code")
        result.msg = json_data.get_string("msg")
        result.amout = json_data.get_float("amount")
        result.type = json_data.get_int("type")

        return result
