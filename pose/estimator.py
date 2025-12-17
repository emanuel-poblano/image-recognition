# MediaPipe wrapper

import cv2
import mediapipe as mp

class PoseEstimator:
    """
    Wrapper for MediaPipe Pose with smoothing and error handling.
    """

    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        try:
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence
            )
            self.mp_draw = mp.solutions.drawing_utils
            self.connections = self.mp_pose.POSE_CONNECTIONS
            print("[INFO] MediaPipe Pose initialized successfully.")
        except AttributeError:
            raise ImportError(
                "MediaPipe installation not found or incompatible. "
                "Run: pip install mediapipe --upgrade"
            )

    def process_frame(self, frame):
        """
        Process a single image frame and return pose landmarks.
        Returns:
            landmarks: List of landmarks or None if not detected.
        """
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            return results.pose_landmarks
        except Exception as e:
            print(f"[ERROR] Failed to process frame: {e}")
            return None

    def draw_landmarks(self, frame, landmarks):
        """
        Draw landmarks and connections on the frame.
        """
        if landmarks is not None:
            self.mp_draw.draw_landmarks(frame, landmarks, self.connections)

    def close(self):
        """
        Release any resources if needed.
        """
        self.pose.close()
        print("[INFO] MediaPipe Pose resources released.")
