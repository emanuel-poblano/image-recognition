import pytest

cv2 = pytest.importorskip("cv2")
from app.camera import Camera, CameraError


class FakeCap:
    def __init__(self, script):
        self.script = list(script)
        self.released = False

    def isOpened(self):
        return self.script is not None

    def read(self):
        return self.script.pop(0) if self.script else (False, None)

    def get(self, _):
        return 0

    def release(self):
        self.released = True


def test_open_failure_raises():
    with pytest.raises(CameraError):
        Camera(0, capture_factory=lambda s: type("C", (), {"isOpened": lambda self: False})())


def test_file_ends_cleanly():
    cam = Camera("x.mp4", capture_factory=lambda s: FakeCap([(True, 1), (True, 2)]))
    assert list(cam.frames()) == [1, 2]


def test_reconnect_after_failures():
    caps = [FakeCap([(True, 1)]), FakeCap([(True, 2)])]
    cam = Camera(0, max_failures=3, reconnect_delay=0, capture_factory=lambda s: caps.pop(0))
    it = cam.frames()
    assert next(it) == 1
    assert next(it) == 2


def test_gives_up_when_reconnect_fails():
    calls = []

    def factory(s):
        calls.append(1)
        return FakeCap([(True, 1)]) if len(calls) == 1 else type("C", (), {"isOpened": lambda self: False})()

    cam = Camera(0, max_failures=2, reconnect_attempts=2, reconnect_delay=0, capture_factory=factory)
    it = cam.frames()
    assert next(it) == 1
    with pytest.raises(CameraError):
        next(it)


def test_recovery_budget_is_not_reset_until_a_frame_arrives():
    calls = []

    def factory(_):
        calls.append(1)
        if len(calls) == 1:
            return FakeCap([(True, 1), (False, None)])
        return FakeCap([])

    cam = Camera(0, max_failures=1, reconnect_attempts=2, reconnect_delay=0,
                 capture_factory=factory)
    frames = cam.frames()
    assert next(frames) == 1
    with pytest.raises(CameraError):
        next(frames)
    assert len(calls) == 3
