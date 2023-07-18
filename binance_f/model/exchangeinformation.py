class RateLimit:

    def __init__(self):
        self.rateLimitType = ""
        self.interval = ""
        self.intervalNum = 0
        self.limit = 0


class ExchangeFilter:

    def __init__(self):
        self.filterType = ""
        self.maxOrders = 0


class Symbol:

    def __init__(self):
        self.symbol = ""
        self.status = ""
        self.maintMarginPercent = 0.0
        self.requiredMarginPercent = 0.0
        self.baseAsset = ""
        self.quoteAsset = ""
        self.pricePrecision = None
        self.quantityPrecision = None
        self.baseAssetPrecision = None
        self.quotePrecision = None
        self.orderTypes = list()
        self.timeInForce = list()
        self.filters = list()




class ExchangeInformation:

    def __init__(self):
        self.timezone = ""
        self.serverTime = 0
        self.rateLimits = list()
        self.exchangeFilters = list()
        self.symbols = list()

    @staticmethod
    def json_parse(json_data):
        result = ExchangeInformation()
        result.timezone = json_data.get_string("timezone")
        result.serverTime = json_data.get_int("serverTime")

        data_list = json_data.get_array("rateLimits")
        element_list = list()
        for item in data_list.get_items():
            element = RateLimit()
            element.rateLimitType = item.get_string("rateLimitType")
            element.interval = item.get_string("interval")
            element.intervalNum = item.get_int("intervalNum")
            element.limit = item.get_int("limit")

            element_list.append(element)
        result.rateLimits = element_list

        data_list = json_data.get_array("exchangeFilters")
        element_list = list()
        for item in data_list.get_items():
            element = ExchangeFilter()
            element.filterType = item.get_string("filterType")
            if element.filterType == "EXCHANGE_MAX_NUM_ORDERS":
                element.maxNumOrders = item.get_int("maxNumOrders")
            elif  element.filterType == "EXCHANGE_MAX_ALGO_ORDERS":
                element.maxNumAlgoOrders = item.get_int("maxNumAlgoOrders")

            element_list.append(element)
        result.exchangeFilters = element_list

        data_list = json_data.get_array("symbols")
        element_list = list()
        for item in data_list.get_items():
            element = Symbol()
            element.symbol = item.get_string("symbol")
            element.status = item.get_string("status")
            element.maintMarginPercent = item.get_float("maintMarginPercent")
            element.requiredMarginPercent = item.get_float("requiredMarginPercent")
            element.baseAsset = item.get_string("baseAsset")
            element.quoteAsset = item.get_string("quoteAsset")
            element.pricePrecision = item.get_int("pricePrecision")
            element.quantityPrecision = item.get_int("quantityPrecision")
            element.baseAssetPrecision = item.get_int("baseAssetPrecision")
            element.quotePrecision = item.get_int("quotePrecision")
            element.orderTypes = item.get_object("orderTypes").convert_2_list()
            element.timeInForce = item.get_object("timeInForce").convert_2_list()

            val_list = item.get_array("filters")
            filter_list = list()
            for jtem in val_list.get_items():
                filter_list.append(jtem.convert_2_dict())
            element.filters = filter_list

            element_list.append(element)
        result.symbols = element_list

        return result

