import numpy as np

def calculate_angle(a, b, c):
    a, b, c = map(np.array, (a, b, c))
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / np.pi)
    return min(angle, 360-angle)
