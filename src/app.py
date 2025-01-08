import os
import threading

import streaming
import recording


# script parent path
my_path = os.path.abspath(os.path.dirname(__file__))

# init logger
# TODO

def main():
    try:
        # start recording
        threading.Thread(target=recording.record_frame, daemon=True).start()

        # start steaming
        streaming.run()

    except Exception as ex:
        print("An exception has occured.")


if __name__ == "__main__":
    main()
