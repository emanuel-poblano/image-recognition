"""Session summary generation."""

import json
import time


class Session:
    def __init__(self, exercise):
        self.exercise = exercise
        self.start = time.time()
        self.frames = 0
        self.tracked_frames = 0
        self.feedback_counts = {}

    def update(self, tracked, feedback=None):
        self.frames += 1
        if tracked:
            self.tracked_frames += 1
            if feedback and feedback != "Good form":
                self.feedback_counts[feedback] = self.feedback_counts.get(feedback, 0) + 1

    def summary(self, duration=None):
        ex = self.exercise
        valid = [r for r in ex.rep_log if r["valid"]]
        depths = [r["min_angle"] for r in valid]
        return {
            "exercise": ex.name,
            "duration_s": round(duration if duration is not None else time.time() - self.start, 1),
            "reps": ex.reps,
            "partial_reps": ex.partial_reps,
            "avg_min_angle": round(sum(depths) / len(depths), 1) if depths else None,
            "tracking_rate": round(self.tracked_frames / self.frames, 3) if self.frames else 0.0,
            "feedback_counts": dict(self.feedback_counts),
        }

    def to_text(self, duration=None):
        s = self.summary(duration)
        lines = [f"Session summary: {s['exercise']}",
                 f"  Duration: {s['duration_s']}s",
                 f"  Reps: {s['reps']} (partial: {s['partial_reps']})",
                 f"  Tracking rate: {s['tracking_rate']:.0%}"]
        if s["avg_min_angle"] is not None:
            lines.append(f"  Avg bottom angle: {s['avg_min_angle']} deg")
        for msg, n in sorted(s["feedback_counts"].items(), key=lambda kv: -kv[1]):
            lines.append(f"  Feedback '{msg}': {n} frames")
        return "\n".join(lines)

    def save(self, path, duration=None):
        with open(path, "w") as f:
            json.dump(self.summary(duration), f, indent=2)
