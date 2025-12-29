import cv2
from pose.estimator import PoseEstimator
from exercises.squat import SquatExercise
from exercises.pushup import PushUpExercise
from feedback.overlay import draw_overlay


def main():
    pose = PoseEstimator()

    exercises = {
        "squat": SquatExercise(),
        "pushup": PushUpExercise(),
    }
    current = "squat"

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("[ERROR] Camera not available")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        landmarks = pose.process_frame(frame)
        if landmarks:
            result = exercises[current].update(landmarks)
            draw_overlay(
                frame,
                exercises[current].name,
                result["reps"],
                result["feedback"],
            )

        cv2.putText(
            frame,
            f"Mode: {current.upper()} (S / P)",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 255),
            2,
        )

        cv2.imshow("Gym Form AI", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            current = "squat"
        elif key == ord("p"):
            current = "pushup"

    cap.release()
    cv2.destroyAllWindows()
    pose.close()


if __name__ == "__main__":
    main()
