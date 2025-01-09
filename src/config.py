import json


class Dict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(object):
    @staticmethod
    def load_data(data):
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        ret = Dict()
        for key, value in data.items():
            ret[key] = Config.load_data(value)
        return ret

    @staticmethod
    def load_list(data: list):
        ret = [Config.load_data(value) for value in data]
        return ret

    @staticmethod
    def load_json(path: str):
        try:
            with open(path, "r") as f:
                ret = Config.load_data(json.loads(f.read()))
            return ret
        except Exception as ex:
            print("An exception has occured.")
