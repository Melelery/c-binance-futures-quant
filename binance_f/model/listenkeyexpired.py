class ListenKeyExpired:
    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
  
    @staticmethod
    def json_parse(json_data):
        result = ListenKeyExpired()
        result.eventType = json_data.get_string("e")
        result.eventTime = json_data.get_int("E")
        
        return result
