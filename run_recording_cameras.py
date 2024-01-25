import cv2
import os
import numpy as np
import time
import queue
import threading


class IPCamera:
    _d_q: queue.Queue  # Display queue
    _r_q: queue.Queue  # Record queue

    """Parameters for Camera Distortion."""
    _K: np.ndarray = np.array(
        [[1490.4374643604199, 0.0, 990.6557248821284], [0.0, 1490.6535480621505, 544.6243597123726], [0.0, 0.0, 1.0]])
    _D: np.ndarray = np.array([[-0.2976428547328032], [3.2508343621538445], [-17.38410840159056], [30.01965021834286]])
    _DIM: tuple[int, int] = (1920, 1080)
    _map1: cv2.typing.MatLike
    _map2: cv2.typing.MatLike


    """Threads for camera functionality."""
    _recieve_thread: threading.Thread
    _display_thread: threading.Thread
    _record_thread: threading.Thread

    _camera_location: str  # Location (address) of the camera
    _is_running: bool  # Allows to break threads



    def __init__(self, camera_location: str, recording_path: str | None = None) -> None:
        """
        Initialize the camera.

        :param camera_location: The location of the camera.
        """
        self._camera_location = camera_location
        self._recording_path = recording_path or f'{time.time()}_output.mp4'

        self._d_q = queue.Queue()
        self._r_q = queue.Queue()

        self._map1, self._map2 = cv2.fisheye.initUndistortRectifyMap(self._K, self._D, np.eye(3), self._K, self._DIM,
                                                         cv2.CV_16SC2)

    def _receive(self) -> None:
        """Recieve data from the camera."""
        cap = cv2.VideoCapture(self._camera_location, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        ret, frame = cap.read()
        frame = self._unfish(frame)

        self._d_q.put(frame)
        self._r_q.put(frame)
        while ret and self._is_running:
            ret, frame = cap.read()
            frame = self._unfish(frame)

            self._d_q.put(frame)
            self._r_q.put(frame)

        else:
            cap.release()

    def _display(self) -> None:
        """Display the data from the camera."""
        while self._is_running:
            if not self._d_q.empty():
                frame = self._d_q.get()
                cv2.imshow("Camera View", frame)
            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()
                self._is_running = False
                break

    def _record(self) -> None:
        out = cv2.VideoWriter(self._recording_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, self._DIM)
        """Record the data from the camera."""
        print("Recording in progress.")
        while self._is_running:
            if not self._r_q.empty():
                out.write(self._r_q.get())
        else:
            out.release()
            print(f"Saving video to: {self._recording_path}")

    def _dump_record(self) -> None:
        """Dump record queue if not used."""
        while self._is_running:
            if not self._r_q.empty():
                self._r_q.get()

    def _dump_display(self) -> None:
        """Dump display queue if not used."""
        while self._is_running:
            if not self._d_q.empty():
                self._d_q.get()

    def _unfish(self, img):
        undistorted = cv2.remap(img, self._map1, self._map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted

    def start(self, record: bool = False, display: bool = True) -> None:
        self._recieve_thread = threading.Thread(target=self._receive)
        self._display_thread = threading.Thread(target=self._display if display else self._dump_display)
        self._record_thread = threading.Thread(target=self._record if record else self._dump_record)

        self._is_running = True

        self._recieve_thread.start()
        self._record_thread.start()
        self._display_thread.start()


if __name__ == '__main__':
    os.environ["XDG_SESSION_TYPE"] = "xcb"
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    address = "your_camera_ip_address"

    camera = IPCamera(camera_location=address, recording_path="camera_stuff/test1_robot.mp4")

    camera.start(display=True, record=False)
