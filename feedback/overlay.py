import cv2


def draw_overlay(frame, exercise_name, reps, feedback):
    cv2.putText(
        frame,
        f"{exercise_name}: {reps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    if feedback:
        cv2.putText(
            frame,
            feedback,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )
