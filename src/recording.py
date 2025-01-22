import os
import time
import cv2 as cv

import logging_wrapper


# Logger
log = logging_wrapper.LoggingWrapper().get_logger(__name__)


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
                log.info(
                    f"Video capture instantiated. IsOpened={video_opened}. BackendName={capture.getBackendName()}."
                )
                while True:
                    # stop if user has requested the app shutdown
                    if shutting_down:
                        break
                    # write video frame
                    write_video_frame(config)
            else:
                log.error(f"Video capture is not opened. IsOpened={video_opened}")
        else:
            log.error("Video capture is None.")
    except Exception as e:
        log.exception(e)
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
                buffer = b""
            else:
                success, buffer = cv.imencode(ext=".jpg", img=frame)
                if not success:
                    log.error("Failed to encode the frame.")
                    continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
            )
    except Exception as e:
        log.exception(e)


# Detect CTRL+C key press
def signal_handler(s, f):
    global shutting_down
    shutting_down = True


def write_video_frame(config):
    """Write video frames to the output file."""
    global writer, frame, frame_count

    try:
        # read frames and write them to a file
        init_video_writer(config)
        if writer:
            log.info(f"Video writer instantiated. Output={output_path}")
            start = time.time()
            while time.time() - start < config.Recording.Duration:
                ret, frame = capture.read()
                if ret:
                    frame_count += 1
                    # add frame text
                    put_frame_text(
                        [
                            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                            f"Camera: {config.Recording.CameraIndex}",
                            f"Frame count: {frame_count}",
                        ]
                    )
                    # write fram
                    writer.write(frame)
                else:
                    log.error(f"Read frame has failed. Flag={ret}")
                    break
            # let go of the writer
            writer.release()
        else:
            log.error("Video writer is None.")
    except Exception as e:
        log.exception(e)
    finally:
        if writer:
            writer.release()


def init_video_writer(config):
    """Create VideoWriter instance"""
    global writer

    init_output_file_path(config)
    width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
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
    name = (
        f"{stamp}_webcam_{config.Recording.CameraIndex}_{config.Recording.OutputName}"
    )
    if config.Recording.OutputPath:
        path = os.path.abspath(config.Recording.OutputPath)
        if not os.path.exists(path):
            os.makedirs(path)
        output_path = os.path.join(path, name)
    else:
        output_path = name


def put_frame_text(lines: list):
    """Puts frame text lines on the frame."""
    if not lines:
        log.info("Text lines are none or empty.")
        return

    font_scale = 0.5
    line_color = (40, 240, 240)  # yellowish color in BGR (hex=#f2ef1e)
    line_thickness = 1
    font_face = cv.FONT_HERSHEY_DUPLEX
    line_type = cv.LINE_AA

    # top-left corner of the frame. bottom-left corner of the text
    text_position = (10, 25)
    text = lines[0]  # first line
    text_size = cv.getTextSize(text, font_face, font_scale, line_thickness)
    line_height = text_size[1] + 12
    x0, y0 = text_position

    for index, line in enumerate(lines):
        y = y0 + index * line_height
        cv.putText(
            frame,
            line,
            (x0, y),
            font_face,
            font_scale,
            line_color,
            line_thickness,
            line_type,
        )
