from exercises.base import ExerciseBase
from analysis.angles import calculate_angle
from mediapipe.python.solutions.pose import PoseLandmark


class SquatExercise(ExerciseBase):
    def __init__(self):
        super().__init__(name="Squat")
        self.state = "up"
        
    def update(self, landmarks):
        hip = landmarks.landmark[PoseLandmark.LEFT_HIP.value]
        knee = landmarks.landmark[PoseLandmark.LEFT_KNEE.value]
        ankle = landmarks.landmark[PoseLandmark.LEFT_ANKLE.value]

        angle = calculate_angle(
            (hip.x, hip.y),
            (knee.x, knee.y),
            (ankle.x, ankle.y),
        )

        feedback = ""

        if angle < 70:
            self.state = "down"
            feedback = "Good depth"
        elif angle > 160 and self.state == "down":
            self.reps += 1
            self.state = "up"
            feedback = "Squat counted!"
        elif angle > 100 and self.state == "up":
            feedback = "Go deeper"

        return {
            "reps": self.reps,
            "feedback": feedback,
            "angle": round(angle, 1),
    }