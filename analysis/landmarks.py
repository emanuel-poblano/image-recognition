"""Convert MediaPipe pose landmarks into the dict format exercises use."""

# MediaPipe Pose landmark indices per body side
SIDES = {
    "left": dict(shoulder=11, elbow=13, wrist=15, hip=23, knee=25, ankle=27),
    "right": dict(shoulder=12, elbow=14, wrist=16, hip=24, knee=26, ankle=28),
}
MIN_VISIBILITY = 0.5


def extract_landmarks(pose_landmarks, required, min_visibility=MIN_VISIBILITY):
    """Return {joint: (x, y)} for the more visible body side, or None if any
    required joint is missing or below min_visibility."""
    if pose_landmarks is None:
        return None
    pts = pose_landmarks.landmark
    best, best_score = None, -1.0
    for idx in SIDES.values():
        vis = [pts[i].visibility for i in idx.values()]
        score = min(pts[idx[j]].visibility for j in required)
        if score >= min_visibility and sum(vis) > best_score:
            best, best_score = idx, sum(vis)
    if best is None:
        return None
    return {j: (pts[i].x, pts[i].y) for j, i in best.items()}
