from abc import ABC, abstractmethod


class ExerciseBase(ABC):
    def __init__(self, name: str):
        self.name = name
        self.reps = 0

    @abstractmethod
    def update(self, landmarks) -> dict:
        """
        Process pose landmarks and return:
        {
            reps: int,
            feedback: str,
            angle: float
        }
        """
        pass
