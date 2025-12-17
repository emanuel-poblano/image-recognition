import cv2

def draw_feedback(frame, text, reps):
    cv2.putText(frame, f"Reps: {reps}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.putText(frame, text, (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
