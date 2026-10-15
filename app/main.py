import argparse
import sys
import time

import cv2

from app.camera import Camera, CameraError
from app.runner import process_frames
from analysis.session import Session
from exercises import EXERCISES
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
    session = Session(EXERCISES[args.exercise]())

    def on_frame(frame, landmarks, feedback, reps):
        pose.draw_landmarks(frame, landmarks)
        draw_feedback(frame, feedback, reps)
        cv2.imshow("Gym Form AI", frame)
        return not (cv2.waitKey(1) & 0xFF == ord("q"))

    status = 0
    try:
        process_frames(cam.frames(), pose, args.exercise, on_frame, session=session)
    except CameraError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        status = 1
    finally:
        cam.release()
        pose.close()
        cv2.destroyAllWindows()

    duration = time.time() - start
    print(session.to_text(duration))
    if args.summary_json:
        session.save(args.summary_json, duration)
    return status


if __name__ == "__main__":
    sys.exit(main())
