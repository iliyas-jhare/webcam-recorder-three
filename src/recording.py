import os
import time
import cv2 as cv

import logging_utils


# Logger
logger = logging_utils.get_logger(__name__)


# Globals
capture = None
frame = None
writer = None
output_path = None
video_opened = False
shutting_down = False


def capture_video_frame(config):
    """Starts recording video frames and also writes to the output files as configured in the config file."""
    global capture, frame, output_path, video_opened

    try:
        capture = cv.VideoCapture(config.Recording.CameraIndex)
        if capture:
            # check if video capture was opened
            video_opened = capture.isOpened()
            if video_opened:
                logger.info(
                    f"Video capture instantiated. IsOpened={video_opened} BackendName={capture.getBackendName()}"
                )
                width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
                height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
                while True:
                    # stop if user has requested the app shutdown
                    if shutting_down:
                        break
                    # read frames and write them to a file
                    init_video_writer(config, width, height)
                    if not writer:
                        break
                    logger.info(f"Video writer instantiated. Output={output_path}")
                    # write video frame
                    write_video_frame(config)
                    # let go of the writer
                    writer.release()
            else:
                logger.error(f"Video capture is not opened. IsOpened={video_opened}")
        else:
            logger.error("Video capture is None.")

    except Exception as e:
        logger.exception(e)

    finally:
        if writer:
            writer.release()
        if capture:
            capture.release()


def get_video_frame():
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


def init_video_writer(config, width, height):
    """Create VideoWriter instance"""
    global writer, output_path

    init_output_file_path(config)
    fourcc = cv.VideoWriter_fourcc(*config.Recording.WriterFourCC)
    fps = config.Recording.FramesPerSecond
    frame_size = (width, height)
    writer = cv.VideoWriter(output_path, fourcc, fps, frame_size)


def init_output_file_path(config):
    """Get unique time stamped video output file name."""
    global output_path

    stamp = time.strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}_{config.Recording.OutputName}"
    if config.Recording.OutputPath:
        path = os.path.abspath(config.Recording.OutputPath)
        if not os.path.exists(path):
            os.makedirs(path)
        output_path = os.path.join(path, name)
    else:
        output_path = name


def write_video_frame(config):
    """Write video frames to the output file."""
    global capture, writer, frame

    if writer:
        start = time.time()
        while time.time() - start < config.Recording.Duration:
            ret, frame = capture.read()
            if ret:
                writer.write(frame)
            else:
                logger.error(f"Read frame has failed. Flag={ret}")
                break

    else:
        logger.error("Video writer is None.")
