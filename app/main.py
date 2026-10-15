import argparse
import sys
import time

import cv2

from app.camera import Camera, CameraError
from app.runner import process_frames
from feedback.overlay import draw_feedback
from pose.estimator import PoseEstimator


def main(argv=None):
    p = argparse.ArgumentParser(description="Gym form correction")
    p.add_argument("--exercise", choices=["squat", "pushup"], default="squat")
    p.add_argument("--source", default="0", help="camera index or video path")
    p.add_argument("--summary-json", help="write session summary to this file")
    args = p.parse_args(argv)
    source = int(args.source) if args.source.isdigit() else args.source

    try:
        cam = Camera(source)
    except CameraError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    pose = PoseEstimator()
    start = time.time()

    def on_frame(frame, landmarks, feedback, reps):
        pose.draw_landmarks(frame, landmarks)
        draw_feedback(frame, feedback, reps)
        cv2.imshow("Gym Form AI", frame)
        return not (cv2.waitKey(1) & 0xFF == ord("q"))

    session = None
    try:
        exercise, session = process_frames(cam.frames(), pose, args.exercise, on_frame)
    except CameraError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
    finally:
        cam.release()
        pose.close()
        cv2.destroyAllWindows()

    if session is not None:
        print(session.to_text(time.time() - start))
        if args.summary_json:
            session.save(args.summary_json, time.time() - start)
    return 0


if __name__ == "__main__":
    sys.exit(main())
