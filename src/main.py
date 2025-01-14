import os
import threading
import argparse
import signal

import logging_utils
import streaming
import recording

from config import Config
from time import sleep


# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")


# Logger
logger = logging_utils.get_logger(__name__)


def get_args():
    """Parse application command arguments"""
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
    threading.Thread(
        target=recording.capture_video_frame, args=[config], daemon=True
    ).start()
    # delay streaming until video capture is opened
    sleep(config.Streaming.VideoCaptureOpenedDelaySec)
    # start streaming
    if recording.video_opened:
        streaming.start(config)
    logger.info("End")


def signal_handler(sig, f):
    """Detect Ctrl+C signal and handler is it in here"""
    if sig == signal.SIGINT:
        recording.signal_handler(sig, f)
        logger.info("Application shutdown. (CTRL+C)")


signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    try:
        main(get_args())
    except Exception as e:
        logger.exception(e)
