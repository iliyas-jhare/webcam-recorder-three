import os
import threading
import argparse

import logging_utils
import streaming
import recording
from config import Config


# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


# Logger
logger = logging_utils.get_logger(__name__)


def get_args():
    parser = argparse.ArgumentParser("Webcam Recorder Streamer")
    parser.add_argument(
        "-p",
        "--config-path",
        type=str,
        required=False,
        help="Webcam recorder streamer config file path",
        default=CONFIG_PATH,
    )
    args = parser.parse_args()
    return args


def main(args):
    logger.info("Start")
    # load config.json
    config = Config.load_json(args.config_path)
    # start recording
    threading.Thread(target=recording.record_frame, args=[config], daemon=True).start()
    # start streaming
    streaming.start(config)
    logger.info("End")


if __name__ == "__main__":
    try:
        main(get_args())
    except Exception as e:
        logger.exception(e)
