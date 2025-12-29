import math


def calculate_angle(a, b, c):
    """
    Calculate angle between three points (normalized coords).
    """
    ax, ay = a
    bx, by = b
    cx, cy = c

    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    angle = abs(radians * 180.0 / math.pi)

    if angle > 180:
        angle = 360 - angle

    return angle
