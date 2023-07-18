
class RestApiRequest(object):

    def __init__(self):
        self.method = ""
        self.url = ""
        self.host = ""
        self.post_body = ""
        self.header = dict()
        self.json_parser = None
        self.header.update({"client_SDK_Version": "binance_futures-1.0.1-py3.7"})

