class Balance:

    def __init__(self):
        self.asset = ""
        self.walletBalance = 0.0
        self.crossWallet = 0.0

    @staticmethod
    def json_parse(json_data):
        result = Balance()
        result.asset = json_data.get_string("a")
        result.walletBalance = json_data.get_float("wb")
        result.crossWallet = json_data.get_float("cw")
        return result


class Position:

    def __init__(self):
        self.symbol = ""
        self.amount = 0.0
        self.entryPrice = 0.0
        self.preFee = 0.0
        self.unrealizedPnl = 0.0
        self.marginType = ""
        self.isolatedWallet = 0.0
        self.positionSide = ""

    @staticmethod
    def json_parse(json_data):
        result = Position()
        result.symbol = json_data.get_string("s")
        result.amount = json_data.get_float("pa")
        result.entryPrice = json_data.get_float("ep")
        result.preFee = json_data.get_float("cr")
        result.unrealizedPnl = json_data.get_float("up")
        result.marginType = json_data.get_string("mt")
        result.isolatedWallet = json_data.get_float("iw")
        result.positionSide = json_data.get_string("ps")
        return result


class AccountUpdate:
    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.transactionTime = 0
        self.balances = list()
        self.positions = list()

    @staticmethod
    def json_parse(json_data):
        result = AccountUpdate()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        result.transactionTime = json_data.get_int("T")

        data_group = json_data.get_object("a")
        
        element_list = list()
        data_list = data_group.get_array("B")
        for item in data_list.get_items():
            element = Balance.json_parse(item)
            element_list.append(element)
        result.balances = element_list
       
        if data_group.contain_key("P"):
            element_list = list()
            data_list = data_group.get_array("P")
            for item in data_list.get_items():
                element = Position.json_parse(item)
                element_list.append(element)
            result.positions = element_list
        return result
