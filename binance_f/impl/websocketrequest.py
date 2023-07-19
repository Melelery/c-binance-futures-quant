class WebsocketRequest(object):

    def __init__(self):
        self.subscription_handler = None
        self.auto_close = False   # close connection after receive data, for subscribe set False, for request set True
        self.is_trading = False
        self.error_handler = None
        self.json_parser = None
        self.update_callback = None
