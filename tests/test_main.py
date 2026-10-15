import json
from types import SimpleNamespace

from app import main as app_main
from app.camera import CameraError


class FakeFrame:
    shape = (100, 200, 3)


def test_camera_failure_saves_partial_session_and_returns_failure(monkeypatch, tmp_path):
    summary_path = tmp_path / "summary.json"

    class FakeCamera:
        def __init__(self, source):
            pass

        def frames(self):
            yield FakeFrame()
            raise CameraError("camera lost")

        def release(self):
            pass

    class FakePose:
        def process_frame(self, frame):
            points = [SimpleNamespace(x=0.0, y=0.0, visibility=0.0)
                      for _ in range(33)]
            for index in (23, 25, 27):
                points[index] = SimpleNamespace(x=0.25, y=0.75, visibility=0.9)
            return SimpleNamespace(landmark=points)

        def draw_landmarks(self, frame, landmarks):
            pass

        def close(self):
            pass

    class FakeExercise:
        name = "squat"
        reps = 0
        partial_reps = 0
        rep_log = []

        def analyze(self, landmarks):
            self.reps += 1
            return "Good form", self.reps

    monkeypatch.setattr(app_main, "Camera", FakeCamera)
    monkeypatch.setattr(app_main, "PoseEstimator", FakePose)
    monkeypatch.setitem(app_main.EXERCISES, "squat", FakeExercise)
    monkeypatch.setattr(app_main, "draw_feedback", lambda *args: None)
    monkeypatch.setattr(app_main.cv2, "imshow", lambda *args: None)
    monkeypatch.setattr(app_main.cv2, "waitKey", lambda *args: -1)
    monkeypatch.setattr(app_main.cv2, "destroyAllWindows", lambda: None)

    result = app_main.main(["--summary-json", str(summary_path)])

    assert result == 1
    summary = json.loads(summary_path.read_text())
    assert summary["reps"] == 1
    assert summary["tracking_rate"] == 1.0
