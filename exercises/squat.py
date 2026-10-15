from exercises.base import Exercise
from analysis.angles import calculate_angle

UP_ANGLE = 160     # knee angle considered standing
DOWN_ANGLE = 100   # knee must go below this for a full-depth rep
START_ANGLE = 140  # knee must go below this to begin a descent


class Squat(Exercise):
    """Knee-angle squat tracker (side view).

    A rep is counted when the user descends past DOWN_ANGLE and returns
    above UP_ANGLE. Descents that begin but never reach depth are logged as
    partial reps and are not counted.
    """
    name = "squat"

    def __init__(self):
        super().__init__()
        self._min_angle = None

    def analyze(self, lm):
        knee_angle = calculate_angle(lm["hip"], lm["knee"], lm["ankle"])
        feedback = "Good form"

        if self.stage is None:
            if knee_angle >= UP_ANGLE:
                self.stage = "up"
            return "Stand tall to begin", self.reps

        if self.stage == "up":
            if knee_angle < START_ANGLE:
                self.stage = "descending"
                self._min_angle = knee_angle
        else:
            self._min_angle = min(self._min_angle, knee_angle)
            if self._min_angle < DOWN_ANGLE:
                self.stage = "down"
                feedback = "Good depth - stand up"
            else:
                feedback = "Go deeper"
            if knee_angle >= UP_ANGLE:
                if self._min_angle < DOWN_ANGLE:
                    self.reps += 1
                    self._log_rep(min_angle=self._min_angle, valid=True)
                else:
                    self.partial_reps += 1
                    self._log_rep(min_angle=self._min_angle, valid=False)
                self.stage = "up"
                self._min_angle = None
                feedback = "Good form"

        if "shoulder" in lm and self.stage in ("descending", "down"):
            # torso lean: angle shoulder-hip-knee; very small = folded forward
            if calculate_angle(lm["shoulder"], lm["hip"], lm["knee"]) < 45:
                feedback = "Keep your chest up"

        return feedback, self.reps
