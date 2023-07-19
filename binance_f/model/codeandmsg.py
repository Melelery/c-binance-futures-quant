class CodeMsg:

    def __init__(self):
        self.code = 0
        self.msg = ""

    @staticmethod
    def json_parse(json_data):
        result = CodeMsg()
        result.code = json_data.get_int("code")
        result.msg = json_data.get_string("msg")

        return result
