class ChannelParser:
    def __init__(self, input):
        fields = input.split(".")
        if len(fields) >= 2:
            self.symbol = fields[1]
