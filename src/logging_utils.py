import logging
import datetime
import os
import sys

from logging import FileHandler, StreamHandler

# logger file init
STAMPPED = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_name = f"{STAMPPED}_webcam.log"
file_path = "./logs"
log_path = os.path.join(os.path.abspath(file_path), file_name)


def create_file_handler(level=logging.INFO) -> FileHandler:
    """Creates new logger file handler instance"""
    path = os.path.abspath(file_path)
    if not os.path.exists(path):
        os.makedirs(path)
    format = "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
    formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(log_path, delay=True)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    return file_handler


def create_stream_handler(level=logging.INFO) -> StreamHandler:
    """Create new logger stream handler instance"""
    format = "[%(levelname)s] [%(filename)s] %(message)s"
    formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name: str, level=logging.INFO):
    """Creates new logger instance with file and stream handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = create_stream_handler(level)
    logger.addHandler(stream_handler)
    file_handler = create_file_handler(level)
    logger.addHandler(file_handler)
    return logger
