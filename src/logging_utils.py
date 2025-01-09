import logging
import datetime


LOGGER_PATH = datetime.datetime.now().strftime(
    "%Y%m%d-%H%M%S_webcam_recorder_streamer.log"
)
LOGGER_FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger_handler = logging.FileHandler(LOGGER_PATH, delay=True)
    logger_formatter = logging.Formatter(LOGGER_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)
    return logger
