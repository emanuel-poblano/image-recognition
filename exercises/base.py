# Abstract exercise class

from abc import ABC, abstractmethod


class Exercise(ABC):
    name = "exercise"

    def __init__(self):
        self.reps = 0
        self.partial_reps = 0
        self.stage = None
        self.rep_log = []  # one dict per completed (or partial) rep

    @abstractmethod
    def analyze(self, landmarks):
        """Return (feedback, reps) for one frame of landmarks."""

    def _log_rep(self, **info):
        self.rep_log.append(info)
