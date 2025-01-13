import os
import time
import cv2 as cv

import logging_utils

from cv2 import VideoWriter

# Logger
logger = logging_utils.get_logger(__name__)


# Globals
capture = None
frame = None
writer = None
video_opened = False
shutting_down = False


def record_frame(config):
    """Starts recording video frames and also writes to the output files as configured in the config file."""
    global frame, writer, video_opened

    try:
        capture = cv.VideoCapture(config.Recording.CameraIndex)
        # check if video capture was opened
        video_opened = capture.isOpened()
        if not video_opened:
            logger.error(
                f"Video capture could not be instantiated. IsOpened={video_opened}"
            )
            return

        logger.info(f"Video capture init. IsOpened={capture.isOpened()}")
        width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))

        while True:
            # stop if user has requested the app shutdown
            if shutting_down:
                break
            # read frames and write them to a file
            writer = get_video_writer(config, width, height)
            start = time.time()
            while time.time() - start < config.Recording.Duration:
                ret, frame = capture.read()
                if not ret:
                    logger.error(f"Read frame has failed. Return={ret}")
                    break
                writer.write(frame)
            # let go of the writer
            writer.release()

    except Exception as e:
        logger.exception(e)

    finally:
        if writer:
            writer.release()
        if capture:
            capture.release()


def get_frame():
    """Starts yielding encoded video frame content."""
    global frame

    try:
        while True:
            if shutting_down:
                break
            if frame is None:
                logger.error("Frame is None.")
                continue
            success, buffer = cv.imencode(".jpg", frame)
            if not success:
                logger.error("Failed to encode the frame.")
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
            )
    except Exception as e:
        logger.exception(e)


# Detect CTRL+C key press
def signal_handler(s, f):
    global shutting_down
    shutting_down = True


def get_output_file_name(config) -> str:
    """Get unique time stamped video output file name."""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}_{config.Recording.OutputName}"
    if config.Recording.OutputPath:
        path = os.path.abspath(config.Recording.OutputPath)
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, name)
    else:
        return name


def get_video_writer(config, width, height) -> VideoWriter:
    """Create VideoWriter instance"""
    file_name = get_output_file_name(config)
    fourcc = cv.VideoWriter_fourcc(*config.Recording.WriterFourCC)
    fps = config.Recording.FramesPerSecond
    frame_size = (width, height)
    writer = cv.VideoWriter(file_name, fourcc, fps, frame_size)
    return writer
