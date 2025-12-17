import cv2
from pose.estimator import PoseEstimator
from feedback.overlay import draw_feedback  # optional if using feedback module

pose = PoseEstimator()

cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Failed to read frame from camera.")
            break

        landmarks = pose.process_frame(frame)
        pose.draw_landmarks(frame, landmarks)

        # Optional feedback
        # draw_feedback(frame, "Good form", 0)

        cv2.imshow("Gym Form AI", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    pose.close()
    cv2.destroyAllWindows()
