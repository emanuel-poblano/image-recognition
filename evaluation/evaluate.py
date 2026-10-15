"""Evaluate rep counting against labelled recorded videos.

Usage: python -m evaluation.evaluate evaluation/labels.json
labels.json: [{"video": "path.mp4", "exercise": "squat", "true_reps": 10,
               "notes": "side view, good light"}, ...]
Reports per-video error, MAE and exact-match rate; known limitations
should be recorded in `notes` and in docs/ACCURACY.md.
"""
import json
import os
import sys

from app.camera import Camera
from app.runner import process_frames
from pose.estimator import PoseEstimator


def evaluate(labels_path):
    base = os.path.dirname(os.path.abspath(labels_path))
    with open(labels_path) as f:
        labels = json.load(f)
    pose = PoseEstimator()
    rows = []
    try:
        for item in labels:
            cam = Camera(os.path.join(base, item["video"]))
            try:
                ex, sess = process_frames(cam.frames(), pose, item["exercise"])
            finally:
                cam.release()
            s = sess.summary(0)
            rows.append({**item, "counted": ex.reps, "error": ex.reps - item["true_reps"],
                         "tracking_rate": s["tracking_rate"]})
    finally:
        pose.close()
    return rows


def report(rows):
    for r in rows:
        print(f"{r['video']:40s} {r['exercise']:7s} true={r['true_reps']:3d} "
              f"counted={r['counted']:3d} err={r['error']:+d} track={r['tracking_rate']:.0%} {r.get('notes','')}")
    if rows:
        mae = sum(abs(r["error"]) for r in rows) / len(rows)
        exact = sum(r["error"] == 0 for r in rows) / len(rows)
        print(f"\nvideos={len(rows)} MAE={mae:.2f} exact-match={exact:.0%}")


if __name__ == "__main__":
    report(evaluate(sys.argv[1]))
