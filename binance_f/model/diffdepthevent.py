class Order:

    def __init__(self):
        self.price = 0.0
        self.qty = 0.0


class DiffDepthEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.transactionTime = 0
        self.symbol = ""
        self.firstUpdateId = None
        self.finalUpdateId = None
        self.lastUpdateIdInlastStream = 0
        self.bids = list()
        self.asks = list()

    @staticmethod
    def json_parse(json_data):
        order_book = DiffDepthEvent()
        order_book.eventType = json_data.get_string("e")
        order_book.eventTime = json_data.get_int("E")
        order_book.transactionTime = json_data.get_int("T")
        order_book.symbol = json_data.get_string("s")
        order_book.firstUpdateId = json_data.get_int("U")
        order_book.finalUpdateId = json_data.get_int("u")
        order_book.lastUpdateIdInlastStream = json_data.get_int("pu")

        list_array = json_data.get_array("b")
        bid_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            bid_list.append(order)
        order_book.bids = bid_list

        list_array = json_data.get_array("a")
        ask_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            ask_list.append(order)
        order_book.asks = ask_list        

        return order_book