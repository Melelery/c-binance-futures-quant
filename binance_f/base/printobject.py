import sys

BASIC_DATA_TYPE = (int, str, float)
BASIC_DATA_TYPE_BOOL = (bool)

TYPE_BASIC = "type_basic"
TYPE_BOOL = "type_bool"
TYPE_OBJECT = "type_object"
TYPE_LIST = "type_list"
TYPE_DICT = "type_dict"
TYPE_UNDEFINED = "type_undefined"


class TypeCheck:
    @staticmethod
    def is_list(obj):
        return type(obj) == list and isinstance(obj, list)

    @staticmethod
    def is_dict(obj):
        return type(obj) == dict and isinstance(obj, dict)

    @staticmethod
    def is_object(obj):
        return isinstance(obj, object)

    @staticmethod
    def is_basic(obj):
        return isinstance(obj, BASIC_DATA_TYPE)

    @staticmethod
    def is_bool(obj):
        return isinstance(obj, bool)

    @staticmethod
    def get_obj_type(obj):
        if TypeCheck.is_basic(obj):
            return TYPE_BASIC
        elif TypeCheck.is_bool(obj):
            return TYPE_BOOL
        elif TypeCheck.is_list(obj):
            return TYPE_LIST
        elif TypeCheck.is_dict(obj):
            return TYPE_DICT
        elif TypeCheck.is_object(obj):
            return TYPE_OBJECT
        else:
            return TYPE_UNDEFINED


class PrintBasic:
    @staticmethod
    def print_basic(data, name=None):
        if name and len(name):
            print(str(name) + " : " + str(data))
        else:
            print(str(data))

    @staticmethod
    def print_basic_bool(data, name=None):
        bool_desc = "True"
        if not data:
            bool_desc = "False"

        if name and len(name):
            print(str(name) + " : " + str(bool_desc))
        else:
            print(str(bool_desc))

    @staticmethod
    def print_obj(obj):
        if not obj:
            return -1

        members = [attr for attr in dir(obj) if not callable(attr) and not attr.startswith("__")]
        for member_def in members:
            val_str = str(getattr(obj, member_def))
            print(member_def + ":" + val_str)
        return 0


class PrintList:
    @staticmethod
    def print_list_data(obj):
        if not obj:
            print("object is None")
            return -1

        if TypeCheck.get_obj_type(obj) == TYPE_LIST:
            for idx, row in enumerate(obj):
                PrintBasic.print_basic(row)
        else:
            return -2

        return 0

    @staticmethod
    def print_origin_object(obj):
        if not obj:
            print("object is None")
            return -1
        obj_type = TypeCheck.get_obj_type(obj)

        if obj_type == TYPE_BASIC:
            PrintBasic.print_basic(obj)
        elif obj_type == TYPE_BOOL:
            PrintBasic.print_basic_bool(obj)
        elif obj_type == TYPE_OBJECT:
            PrintBasic.print_obj(obj)
        else:
            return 1

        return 0

    @staticmethod
    def print_object_list(obj_list):
        if not obj_list:
            return -1

        obj_type = TypeCheck.get_obj_type(obj_list)
        if obj_type != TYPE_LIST:
            return -2

        print ("data count : ", (len(obj_list)))
        print ("\n")
        for idx, row in enumerate(obj_list):
            print("data number " + (str(idx)) + " :")
            PrintList.print_origin_object(row)
            print("\n")
        print("\n\n")

        return 0

    @staticmethod
    def print_object_dict(obj_dict):
        if not obj_dict:
            return -1

        obj_type = TypeCheck.get_obj_type(obj_dict)
        if obj_type != TYPE_DICT:
            return -2

        print ("data count : ", (len(obj_dict)))
        print ("\n")
        for key, row in obj_dict.items():
            PrintBasic.print_basic(str(key) + " :")
            PrintList.print_origin_object(row)
            print("\n")
        print("\n\n")

        return 0


class PrintMix:
    @staticmethod
    def print_data(data):
        if not data:
            print (sys._getframe().f_code.co_name + " none data")
            return -1

        obj_type = TypeCheck.get_obj_type(data)

        if obj_type == TYPE_BASIC:
            PrintBasic.print_basic(data)
        elif obj_type == TYPE_BOOL:
            PrintBasic.print_basic_bool(data)
        elif obj_type == TYPE_LIST:
            PrintList.print_object_list(data)
        elif obj_type == TYPE_DICT:
            PrintList.print_object_dict(data)
        elif obj_type == TYPE_OBJECT:
            PrintList.print_origin_object(data)
        else:
            print (sys._getframe().f_code.co_name + " enter unknown")
            return -2

        return 0


if __name__ == "__main__":
    """
    from binance_f.model.symbol import Symbol

    symbol_1 = Symbol()
    symbol_1.amount_precision = 10009
    symbol_1.symbol = "btcusdt"

    symbol_2 = Symbol()
    symbol_2.amount_precision = 28
    symbol_2.symbol = "htusdt"

    symbol_3 = Symbol()
    symbol_3.amount_precision = 26
    symbol_3.symbol = "eosusdt"

    symbol_list = [symbol_1, symbol_2, symbol_3]
    symbol_dict = {"one": symbol_1, "two": symbol_2, "three": symbol_3}
    PrintMix.print_data(symbol_list)
    PrintMix.print_data(symbol_dict)

    print(type(symbol_list) == list)
    print(type(symbol_dict) == dict)
    print(type(symbol_list) == object)
    print(isinstance(symbol_list, list))
    print(isinstance(symbol_list, object))
    print(isinstance(symbol_dict, dict))
    print(isinstance(symbol_dict, object))
    """

    a=['s', 'h', 'i']
    PrintList.print_list_data(a)
