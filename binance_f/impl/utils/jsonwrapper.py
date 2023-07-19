import json
from binance_f.exception.binanceapiexception import BinanceApiException

class JsonWrapper:
    def __init__(self, json_object):
        self.json_object = json_object

    def __check_mandatory_field(self, name):
        if name not in self.json_object:
            raise BinanceApiException(BinanceApiException.RUNTIME_ERROR,
                                    "[Json] Get json item field: " + name + " does not exist")

    def contain_key(self, name):
        if name in self.json_object:
            return True
        else:
            return False

    def get_boolean(self, name):
        self.__check_mandatory_field(name)
        return bool(self.json_object[name])

    def get_string(self, name):
        self.__check_mandatory_field(name)
        return str(self.json_object[name])

    def get_int(self, name):
        self.__check_mandatory_field(name)
        return int(self.json_object[name])

    def get_string_or_default(self, name, default):
        if self.contain_key(name):
            return str(self.json_object[name])
        else:
            return default

    def get_int_or_default(self, name, default):
        if self.contain_key(name):
            return int(self.json_object[name])
        else:
            return default

    def get_float(self, name):
        self.__check_mandatory_field(name)
        return float(self.json_object[name])

    def get_float_or_default(self, name, default):
        if self.contain_key(name):
            return float(self.json_object[name])
        else:
            return default

    def get_object(self, name):
        self.__check_mandatory_field(name)
        return JsonWrapper(self.json_object[name])

    def get_object_or_default(self, name, defalut_value):
        if name not in self.json_object:
            return defalut_value
        else:
            return JsonWrapper(self.json_object[name])

    def get_array(self, name):
        self.__check_mandatory_field(name)
        return JsonWrapperArray(self.json_object[name])

    def convert_2_array(self):
        return JsonWrapperArray(self.json_object)

    def convert_2_dict(self):
        items = dict()
        for item in self.json_object:
            name = item
            items[name] = self.json_object[name]
        return items

    def convert_2_list(self):
        items = list()
        for item in self.json_object:
            items.append(item)
        return items



class JsonWrapperArray:
    def __init__(self, json_object):
        self.json_object = json_object

    def get_items(self):
        items = list()
        for item in self.json_object:
            items.append(JsonWrapper(item))
        return items

    def get_items_as_array(self):
        items = list()
        for item in self.json_object:
            items.append(JsonWrapperArray(item))
        return items

    def get_float_at(self, index):
        return float(self.json_object[index])

    def get_items_as_string(self):
        items = list()
        for item in self.json_object:
            items.append(str(item))
        return items

    def get_array_at(self, index):
        return JsonWrapperArray(self.json_object[index])

    def get_object_at(self, index):
        return JsonWrapper(self.json_object[index])


