import json

from evaluation import evaluate as evaluation


def test_evaluation_creates_a_fresh_pose_estimator_for_each_video(monkeypatch, tmp_path):
    labels_path = tmp_path / "labels.json"
    labels_path.write_text(json.dumps([
        {"video": "first.mp4", "exercise": "squat", "true_reps": 0},
        {"video": "second.mp4", "exercise": "squat", "true_reps": 0},
    ]))
    estimators = []

    class FakePose:
        def __init__(self):
            self.closed = False
            estimators.append(self)

        def close(self):
            self.closed = True

    class FakeCamera:
        def __init__(self, source):
            self.source = source

        def frames(self):
            return iter(())

        def release(self):
            pass

    class FakeExercise:
        reps = 0

    class FakeSession:
        def summary(self, duration):
            return {"tracking_rate": 1.0}

    monkeypatch.setattr(evaluation, "PoseEstimator", FakePose)
    monkeypatch.setattr(evaluation, "Camera", FakeCamera)
    monkeypatch.setattr(
        evaluation, "process_frames", lambda *args: (FakeExercise(), FakeSession())
    )

    rows = evaluation.evaluate(str(labels_path))

    assert len(rows) == 2
    assert len(estimators) == 2
    assert estimators[0] is not estimators[1]
    assert all(estimator.closed for estimator in estimators)
