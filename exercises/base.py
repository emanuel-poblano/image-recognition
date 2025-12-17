# Abstract exercise class

from abc import ABC, abstractmethod

class Exercise(ABC):
    def __init__(self):
        self.reps = 0
        self.stage = None

    @abstractmethod
    def analyze(self, landmarks):
        pass
