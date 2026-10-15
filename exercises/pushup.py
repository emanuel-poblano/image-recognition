from exercises.base import Exercise
from analysis.angles import calculate_angle

UP_ANGLE = 155     # elbow extended
DOWN_ANGLE = 90    # elbow flexed enough for full depth
START_ANGLE = 135
BODY_LINE_MIN = 150  # shoulder-hip-ankle; below this the hips sag or pike


class PushUp(Exercise):
    """Elbow-angle push-up tracker (side view).

    Counts a rep on full depth then lockout; shallow descents are logged as
    partial. Flags hip sag/pike through the shoulder-hip-ankle angle.
    """
    name = "pushup"

    def __init__(self):
        super().__init__()
        self._min_angle = None
        self._body_ok = True

    def analyze(self, lm):
        elbow = calculate_angle(lm["shoulder"], lm["elbow"], lm["wrist"])
        feedback = "Good form"

        body_ok = True
        if "hip" in lm and "ankle" in lm:
            body_ok = calculate_angle(lm["shoulder"], lm["hip"], lm["ankle"]) >= BODY_LINE_MIN
            if not body_ok:
                feedback = "Keep your body in a straight line"

        if self.stage is None:
            if elbow >= UP_ANGLE:
                self.stage = "up"
            return "Get into plank position", self.reps

        if self.stage == "up":
            if elbow < START_ANGLE:
                self.stage = "descending"
                self._min_angle = elbow
                self._body_ok = body_ok
        else:
            self._min_angle = min(self._min_angle, elbow)
            self._body_ok = self._body_ok and body_ok
            if self._min_angle < DOWN_ANGLE:
                self.stage = "down"
            elif body_ok:
                feedback = "Lower your chest more"
            if elbow >= UP_ANGLE:
                valid = self._min_angle < DOWN_ANGLE
                if valid:
                    self.reps += 1
                else:
                    self.partial_reps += 1
                self._log_rep(min_angle=self._min_angle, valid=valid,
                              body_line_ok=self._body_ok)
                self.stage = "up"
                self._min_angle = None

        return feedback, self.reps
