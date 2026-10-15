# Webcam/video handling
import time

import cv2


class CameraError(RuntimeError):
    pass


class Camera:
    """VideoCapture wrapper: raises CameraError on open failure and
    reconnects after consecutive read failures (live cameras only)."""

    def __init__(self, source=0, max_failures=30, reconnect_attempts=3,
                 reconnect_delay=1.0, capture_factory=cv2.VideoCapture):
        self.source = source
        self.max_failures = max_failures
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self._factory = capture_factory
        self.is_file = isinstance(source, str)
        self.cap = None
        self._open()

    def _open(self):
        cap = self._factory(self.source)
        if cap is None or not cap.isOpened():
            raise CameraError(f"Cannot open video source {self.source!r}")
        self.cap = cap

    def fps(self):
        v = self.cap.get(cv2.CAP_PROP_FPS) if self.cap else 0
        return v if v and v > 0 else 30.0

    def frames(self):
        """Yield frames until end of file / unrecoverable failure."""
        failures = 0
        recovery_attempts = 0
        while True:
            ok, frame = self.cap.read()
            if ok and frame is not None:
                failures = 0
                recovery_attempts = 0
                yield frame
                continue
            if self.is_file:
                return  # end of video
            failures += 1
            if failures < self.max_failures:
                continue
            failures = 0
            while recovery_attempts < self.reconnect_attempts:
                recovery_attempts += 1
                if self._reconnect():
                    break
            else:
                raise CameraError("Camera disconnected and could not be reopened")

    def _reconnect(self):
        self.release()
        time.sleep(self.reconnect_delay)
        try:
            self._open()
            return True
        except CameraError:
            return False

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
