import math
import random

from exercises.pushup import PushUp
from exercises.squat import Squat
from analysis.session import Session


def pt(center, length, deg):
    r = math.radians(deg)
    return (center[0] + length * math.cos(r), center[1] + length * math.sin(r))


def squat_frame(knee_angle):
    knee = (0.0, 0.0)
    return {"hip": pt(knee, 1, 90), "knee": knee, "ankle": pt(knee, 1, 90 - knee_angle)}


def pushup_frame(elbow_angle, body_ok=True):
    elbow = (0.0, 0.0)
    shoulder = pt(elbow, 1, 90)
    hip = (shoulder[0] + 1, shoulder[1])
    ankle = (hip[0] + 1, hip[1] if body_ok else hip[1] + 0.8)
    return {"shoulder": shoulder, "elbow": elbow, "wrist": pt(elbow, 1, 90 - elbow_angle),
            "hip": hip, "ankle": ankle}


def trace(top, bottom, n_reps, steps=10):
    seq = [top] * 5
    for _ in range(n_reps):
        seq += [top + (bottom - top) * i / steps for i in range(steps + 1)]
        seq += [bottom + (top - bottom) * i / steps for i in range(steps + 1)]
    return seq + [top] * 5


def run(ex, frames, seq):
    out = None
    for a in seq:
        out = ex.analyze(frames(a))
    return out


def test_squat_counts_full_reps():
    ex = Squat()
    run(ex, squat_frame, trace(175, 70, 5))
    assert ex.reps == 5 and ex.partial_reps == 0


def test_squat_partial_not_counted():
    ex = Squat()
    run(ex, squat_frame, trace(175, 120, 3))
    assert ex.reps == 0 and ex.partial_reps == 3
    assert not ex.rep_log[0]["valid"]


def test_squat_noise_tolerant():
    random.seed(1)
    ex = Squat()
    run(ex, squat_frame, [a + random.uniform(-4, 4) for a in trace(175, 75, 6)])
    assert ex.reps == 6


def test_squat_standing_still_and_jitter_no_reps():
    ex = Squat()
    run(ex, squat_frame, [170 + random.uniform(-5, 5) for _ in range(200)])
    assert ex.reps == 0


def test_squat_no_count_until_standing():
    ex = Squat()
    fb, _ = ex.analyze(squat_frame(90))
    assert ex.reps == 0 and ex.stage is None


def test_squat_feedback_go_deeper():
    ex = Squat()
    seq = trace(175, 120, 1)
    fbs = [ex.analyze(squat_frame(a))[0] for a in seq]
    assert "Go deeper" in fbs


def test_pushup_counts_full_reps():
    ex = PushUp()
    run(ex, pushup_frame, trace(170, 70, 4))
    assert ex.reps == 4 and ex.rep_log[0]["body_line_ok"]


def test_pushup_partial_and_sag():
    ex = PushUp()
    run(ex, pushup_frame, trace(170, 120, 2))
    assert ex.reps == 0 and ex.partial_reps == 2
    ex = PushUp()
    fbs = [ex.analyze(pushup_frame(a, body_ok=False))[0] for a in trace(170, 70, 1)]
    assert ex.reps == 1 and not ex.rep_log[0]["body_line_ok"]
    assert "Keep your body in a straight line" in fbs


def test_session_summary():
    ex = Squat()
    s = Session(ex)
    for a in trace(175, 70, 3):
        fb, _ = ex.analyze(squat_frame(a))
        s.update(True, fb)
    s.update(False)
    out = s.summary(12.0)
    assert out["reps"] == 3 and out["duration_s"] == 12.0
    assert 0 < out["tracking_rate"] < 1 and out["avg_min_angle"] < 100
    assert "Reps: 3" in s.to_text(12.0)
