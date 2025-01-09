import os
import threading
import argparse

import streaming
import recording

from config import Config

HERE = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")

# init logger
# TODO


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


def main(config):
    # start recording
    thread = threading.Thread(target=recording.record_frame, args=[config], daemon=True)
    thread.start()

    # start steaming
    streaming.run(config)


if __name__ == "__main__":
    try:
        args = get_args()
        config = Config.load_json(args.config_path)
        main(config)
    except Exception as ex:
        print("An exception has occured.")
