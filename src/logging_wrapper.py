import logging
import datetime
import os
import sys


HERE = os.path.abspath(os.path.dirname(__file__))
LOGS_PATH = os.path.join(HERE, "logs")


class LoggingWrapper:
    _instances = {}

    def __init__(self, logs_path=LOGS_PATH):
        self.logs_path = logs_path
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)
        self.file_name = (
            f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}_webcam.log"
        )
        self.file_path = os.path.join(os.path.abspath(self.logs_path), self.file_name)

    def __new__(cls, file_path=LOGS_PATH):
        """Creates singleton object, if it is not instantiated,
        or else returns the previous singleton object"""
        if cls not in cls._instances:
            cls._instances[cls] = super(LoggingWrapper, cls).__new__(cls)
        return cls._instances[cls]

    def create_file_handler(self, level=logging.INFO):
        """Creates new logger file handler instance"""
        format = "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
        formatter = logging.Formatter(format)
        file_handler = logging.FileHandler(self.file_path, delay=True)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        return file_handler

    def create_stream_handler(self, level=logging.INFO):
        """Create new logger stream handler instance"""
        format = "[%(levelname)s] [%(filename)s] %(message)s"
        formatter = logging.Formatter(format)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        return stream_handler

    def get_logger(self, name: str, level=logging.INFO):
        """Creates new logger instance with file and stream handlers"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        stream_handler = self.create_stream_handler(level)
        logger.addHandler(stream_handler)
        file_handler = self.create_file_handler(level)
        logger.addHandler(file_handler)
        return logger
