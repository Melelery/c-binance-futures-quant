import json
from binance_f.impl.utils.jsonwrapper import JsonWrapper


def parse_json_from_string(value):
    value = value.replace("False","false")
    value = value.replace("True","true")
    return JsonWrapper(json.loads(value))
