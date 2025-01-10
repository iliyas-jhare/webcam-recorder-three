import signal

import cv2 as cv

import logging_utils

# Logger
logger = logging_utils.get_logger(__name__)


# Globals
frame = None
shutting_down = False


# Detect CTRL+C key press
def signal_handler(s, f):
    global shutting_down
    shutting_down = True
    logger.info(f"Shutdown (CTRL+C) requested. Flag={shutting_down}")


signal.signal(signal.SIGINT, signal_handler)


def record_frame(config):
    global frame

    try:
        cap = cv.VideoCapture(config.Recording.CameraIndex)
        if cap.isOpened():
            logger.info(f"Video capture init. IsOpened={cap.isOpened()}")
        else:
            logger.error(f"Video capture init. IsOpened={cap.isOpened()}")

        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv.VideoWriter_fourcc(*"XVID")

        while True:
            if shutting_down:
                break
            ret, frame = cap.read()
            if not ret:
                logger.error(f"Read frame. Return={ret}")
                break
    except Exception as e:
        logger.exception(e)
    finally:
        cap.release()


def get_frame():
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
