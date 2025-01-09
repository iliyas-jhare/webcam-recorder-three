import cv2 as cv
import logging_utils

# Logger
logger = logging_utils.get_logger(__name__)


frame = None


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
            if frame is None:
                logger.error("Frame is None here.")
                continue
            success, buffer = cv.imencode(".jpg", frame)
            if not success:
                logger.error("Failed to encode frame.")
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
            )
    except Exception as e:
        logger.exception(e)
