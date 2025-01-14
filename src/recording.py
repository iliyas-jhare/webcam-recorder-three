import os
import time
import cv2 as cv

import logging_utils


# Logger
logger = logging_utils.get_logger(__name__)


# Globals
capture = None
frame = None
frame_count = 0
writer = None
output_path = None
video_opened = False
shutting_down = False


def capture_video_frame(config):
    """Starts recording video frames and also writes to the output files as configured in the config file."""
    global capture, video_opened

    try:
        capture = cv.VideoCapture(index=config.Recording.CameraIndex)
        if capture:
            # check if video capture was opened
            video_opened = capture.isOpened()
            if video_opened:
                logger.info(
                    f"Video capture instantiated. IsOpened={video_opened}. BackendName={capture.getBackendName()}."
                )
                while True:
                    # stop if user has requested the app shutdown
                    if shutting_down:
                        break
                    # write video frame
                    write_video_frame(
                        config=config,
                        width=int(capture.get(cv.CAP_PROP_FRAME_WIDTH)),
                        height=int(capture.get(cv.CAP_PROP_FRAME_HEIGHT)),
                    )
            else:
                logger.error(f"Video capture is not opened. IsOpened={video_opened}")
        else:
            logger.error("Video capture is None.")
    except Exception as e:
        logger.exception(e)
    finally:
        if capture:
            capture.release()


def get_video_frame():
    """Yields encoded video frame content."""
    global frame

    try:
        while True:
            if shutting_down:
                break
            if frame is None:
                logger.error("Frame is None.")
                continue
            success, buffer = cv.imencode(ext=".jpg", img=frame)
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


def write_video_frame(config, width, height):
    """Write video frames to the output file."""
    global writer, frame

    try:
        # read frames and write them to a file
        init_video_writer(config, width, height)
        if writer:
            logger.info(f"Video writer instantiated. Output={output_path}")
            start = time.time()
            while time.time() - start < config.Recording.Duration:
                ret, frame = capture.read()
                if ret:
                    # add frame text
                    put_frame_text()
                    # write fram
                    writer.write(frame)
                else:
                    logger.error(f"Read frame has failed. Flag={ret}")
                    break
            # let go of the writer
            writer.release()
        else:
            logger.error("Video writer is None.")
    except Exception as e:
        logger.exception(e)
    finally:
        if writer:
            writer.release()


def init_video_writer(config, width, height):
    """Create VideoWriter instance"""
    global writer

    init_output_file_path(config)
    writer = cv.VideoWriter(
        filename=output_path,
        fourcc=cv.VideoWriter_fourcc(*config.Recording.WriterFourCC),
        fps=config.Recording.FramesPerSecond,
        frameSize=(width, height),
    )


def init_output_file_path(config):
    """Creates unique time stamped video output file name."""
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


def put_frame_text():
    """Puts frame text on the frame."""
    global frame_count
    frame_count += 1
    cv.putText(
        img=frame,
        text=f"Frame {frame_count}",
        org=(10, 35),
        fontFace=cv.FONT_HERSHEY_DUPLEX,
        fontScale=1,
        color=(0, 0, 0),
        thickness=1,
        lineType=cv.LINE_AA,
    )
