# Accuracy and known limitations

## What is validated today
- `tests/test_exercises.py` replays **synthetic joint-angle traces** (clean reps,
  partial reps, noisy jitter, dropout, standing still) through the squat and
  push-up trackers and checks exact rep counts. This validates the counting logic
  only, **not** MediaPipe accuracy on real footage.
- `tests/test_camera.py` covers camera open failure, mid-stream disconnect/reconnect and
  end-of-file handling with fake captures.

## Real-video validation (TODO: needs recorded footage)
No recorded videos are checked in. To produce real numbers:
1. Record clips (side view, full body in frame; vary lighting, clothing, distance, angle).
2. Hand-count reps and list them in `evaluation/labels.json`.
3. Run `python -m evaluation.evaluate evaluation/labels.json` and paste the output below.

| Video | Exercise | True | Counted | Notes |
|-------|----------|------|---------|-------|
| _none recorded yet_ | | | | |

## Known limitations
- 2D angles: only valid from a side view; front/oblique views distort angles.
- Thresholds (squat bottom <100°, push-up bottom <90°) are fixed, not per-user.
- Occluded limbs: frames below 0.5 landmark visibility are skipped, so fast reps
  during tracking loss can be missed.
- Single person only; deadlift is not implemented.
