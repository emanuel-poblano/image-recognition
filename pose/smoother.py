# Landmark smoothing

from collections import deque
import numpy as np

class LandmarkSmoother:
    def __init__(self, window=5):
        self.history = {}
        self.window = window

    def smooth(self, idx, point):
        if idx not in self.history:
            self.history[idx] = deque(maxlen=self.window)

        self.history[idx].append(point)
        return np.mean(self.history[idx], axis=0)
