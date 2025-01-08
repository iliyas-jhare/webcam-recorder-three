import cv2 as cv


# TODO place in recording config
camera_index = 0
framesPerSecond = 30.0
output_filename_seed = "webcam_output"


frame = None


def record_frame():
    global frame

    cap = cv.VideoCapture(camera_index)
    print(f"Video capture. IsOpened={cap.isOpened()}")

    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv.VideoWriter_fourcc(*"XVID")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Read frame. Return={ret}")
            break

    cap.release()


def get_frame():
    global frame

    while True:
        if frame is None:
            print("Frame is None. Skipping.")
            continue
        success, buffer = cv.imencode(".jpg", frame)
        if not success:
            print("Failed to encode frame.")
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpg\r\n\r\n" + bytearray(buffer) + b"\r\n\r\n"
        )
