class PositionMode:

    def __init__(self):
        self.dualSidePosition = None

    @staticmethod
    def json_parse(json_data):
        result = PositionMode()
        result.dualSidePosition = json_data.get_boolean("dualSidePosition")

        return result
