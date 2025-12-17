from exercises.base import Exercise
from analysis.angles import calculate_angle

class Squat(Exercise):
    def analyze(self, lm):
        hip = lm["hip"]
        knee = lm["knee"]
        ankle = lm["ankle"]

        knee_angle = calculate_angle(hip, knee, ankle)

        feedback = "Good form"

        if knee_angle > 140:
            self.stage = "up"
        if knee_angle < 90 and self.stage == "up":
            self.stage = "down"
            self.reps += 1

        if knee_angle > 120:
            feedback = "Go deeper"

        return feedback, self.reps
