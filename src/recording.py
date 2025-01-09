import cv2 as cv


frame = None


def record_frame(config):
    global frame

    try:
        cap = cv.VideoCapture(config.Recording.CameraIndex)
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
    except Exception as ex:
        print(f"An exception has occured.")
        cap.release()

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
