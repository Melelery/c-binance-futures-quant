class Order:

    def __init__(self):
        self.price = 0.0
        self.qty = 0.0


class OrderBook:

    def __init__(self):
        self.lastUpdateId = 0
        self.bids = list()
        self.asks = list()

    @staticmethod
    def json_parse(json_data):
        order_book = OrderBook()
        order_book.lastUpdateId = json_data.get_int("lastUpdateId")

        list_array = json_data.get_array("bids")
        bid_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            bid_list.append(order)
        order_book.bids = bid_list

        list_array = json_data.get_array("asks")
        ask_list = list()
        for item in list_array.get_items():
            order = Order()
            val = item.convert_2_list()
            order.price = val[0]
            order.qty = val[1]
            ask_list.append(order)
        order_book.asks = ask_list        

        return order_book