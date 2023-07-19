class Asset:

    def __init__(self):
        self.asset = ""
        self.initialMargin = 0.0
        self.maintMargin = 0.0
        self.marginBalance = 0.0
        self.maxWithdrawAmount = 0.0
        self.openOrderInitialMargin = 0.0
        self.positionInitialMargin = 0.0
        self.unrealizedProfit = 0.0
        self.walletBalance = 0.0

    @staticmethod
    def json_parse(json_data):
        result = Asset()
        result.asset = json_data.get_string("asset")
        result.initialMargin = json_data.get_float("initialMargin")
        result.maintMargin = json_data.get_float("maintMargin")
        result.marginBalance = json_data.get_float("marginBalance")
        result.maxWithdrawAmount = json_data.get_float("maxWithdrawAmount")
        result.openOrderInitialMargin = json_data.get_float("openOrderInitialMargin")
        result.positionInitialMargin = json_data.get_float("positionInitialMargin")
        result.unrealizedProfit = json_data.get_float("unrealizedProfit")
        return result


class Position:

    def __init__(self):
        self.initialMargin = 0.0
        self.maintMargin = 0.0
        self.openOrderInitialMargin = 0.0
        self.positionInitialMargin = 0.0
        self.symbol = ""
        self.leverage = 0.0
        self.unrealizedProfit = 0.0
        self.isolated = False
        self.positionSide = ""

    @staticmethod
    def json_parse(json_data):
        result = Position()
        result.initialMargin = json_data.get_float("initialMargin")
        result.maintMargin = json_data.get_float("maintMargin")
        result.leverage = json_data.get_float("leverage")
        result.openOrderInitialMargin = json_data.get_float("openOrderInitialMargin")
        result.positionInitialMargin = json_data.get_float("positionInitialMargin")
        result.symbol = json_data.get_string("symbol")
        result.unrealizedProfit = json_data.get_float("unrealizedProfit")
        result.isolated = json_data.get_boolean("isolated")
        result.positionSide = json_data.get_string("positionSide")
        return result


class AccountInformation:
    def __init__(self):
        self.canDeposit = False
        self.canTrade = False
        self.canWithdraw = False
        self.feeTier = 0
        self.maxWithdrawAmount = 0.0
        self.totalInitialMargin = 0.0
        self.totalMaintMargin = 0.0
        self.totalMarginBalance = 0.0
        self.totalOpenOrderInitialMargin = 0.0
        self.totalPositionInitialMargin = 0.0
        self.totalUnrealizedProfit = 0.0
        self.totalWalletBalance = 0.0
        self.updateTime = 0
        self.assets = list()
        self.positions = list()

    @staticmethod
    def json_parse(json_data):
        result = AccountInformation()
        result.canDeposit = json_data.get_boolean("canDeposit")
        result.canTrade = json_data.get_boolean("canTrade")
        result.canWithdraw = json_data.get_boolean("canWithdraw")
        result.feeTier = json_data.get_float("feeTier")
        result.maxWithdrawAmount = json_data.get_float("maxWithdrawAmount")
        result.totalInitialMargin = json_data.get_float("totalInitialMargin")
        result.totalMaintMargin = json_data.get_float("totalMaintMargin")
        result.totalMarginBalance = json_data.get_float("totalMarginBalance")
        result.totalOpenOrderInitialMargin = json_data.get_float("totalOpenOrderInitialMargin")
        result.totalPositionInitialMargin = json_data.get_float("totalPositionInitialMargin")
        result.totalUnrealizedProfit = json_data.get_float("totalUnrealizedProfit")
        result.totalWalletBalance = json_data.get_float("totalWalletBalance")
        result.updateTime = json_data.get_int("updateTime")
        
        element_list = list()
        data_list = json_data.get_array("assets")
        for item in data_list.get_items():
            element = Asset.json_parse(item)
            element_list.append(element)
        result.assets = element_list
        
        element_list = list()
        data_list = json_data.get_array("positions")
        for item in data_list.get_items():
            element = Position.json_parse(item)
            element_list.append(element)
        result.positions = element_list

        return result
