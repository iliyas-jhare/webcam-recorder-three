import json
import logging_wrapper

# Logger
log = logging_wrapper.LoggingWrapper.get_logger_instance(__name__)


class Dict(dict):
    """Make dictionary items accessible using dot notation"""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(object):
    @staticmethod
    def load_data(data):
        """Loads data from JSON"""
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        """Loads dictionary data from JSON"""
        ret = Dict()
        for key, value in data.items():
            ret[key] = Config.load_data(value)
        return ret

    @staticmethod
    def load_list(data: list):
        """Loads list data from JSON"""
        ret = [Config.load_data(value) for value in data]
        return ret

    @staticmethod
    def load_json(path: str):
        """Load JSON from path provided"""
        try:
            with open(path, "r") as f:
                ret = Config.load_data(json.loads(f.read()))
            return ret
        except Exception as e:
            log.exception(e)
