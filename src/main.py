import sys
import os
import threading
import argparse
import signal

import logging_wrapper
import streaming
import recording

from config import Config


# Constants
CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), "config.json")

# Logger
log = logging_wrapper.LoggingWrapper.get_logger_instance(__name__)


def get_args():
    """Parse application command arguments"""
    parser = argparse.ArgumentParser("Webcam Recorder-Streamer")
    parser.add_argument(
        "-p",
        "--config-path",
        type=str,
        required=False,
        help="Webcam recorder-streamer config file path",
        default=CONFIG_PATH,
    )
    args = parser.parse_args()
    return args


def main(args):
    # logger
    log.info(f"Start. File handler outputting to the path={logging_wrapper.LOGS_PATH}")
    # load config.json
    config = Config.load_json(args.config_path)
    if config:
        # start recording
        threading.Thread(
            target=recording.capture_video_frame, args=[config], daemon=True
        ).start()
        # start streaming
        streaming.init(config)
    else:
        log.error(f"Config could not be loaded. Path={args.config_path}")
    log.info("End")


def signal_handler(sig, f):
    """Detect and handle Ctrl+C signal"""
    recording.signal_handler(sig, f)
    log.info("Application shutdown. (CTRL+C)")
    sys.exit()


signal.signal(signal.SIGTERM, signal_handler)


if __name__ == "__main__":
    try:
        main(get_args())
    except Exception as e:
        log.exception(e)
