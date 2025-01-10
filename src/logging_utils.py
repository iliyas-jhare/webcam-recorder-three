import logging
import datetime
import sys


LOGGER_PATH = datetime.datetime.now().strftime(
    "%Y%m%d-%H%M%S_webcam_recorder_streamer.log"
)


def create_file_handler(level=logging.INFO):
    format = "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
    formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(LOGGER_PATH, delay=True)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    return file_handler


def create_stream_handler(level=logging.INFO):
    format = "[%(levelname)s] [%(filename)s] %(message)s"
    formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = create_stream_handler(level)
    logger.addHandler(stream_handler)
    file_handler = create_file_handler(level)
    logger.addHandler(file_handler)
    return logger
