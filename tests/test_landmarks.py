from types import SimpleNamespace

from analysis.landmarks import extract_landmarks


def test_landmarks_are_pixel_scaled_and_low_visibility_joints_are_omitted():
    points = [SimpleNamespace(x=0.0, y=0.0, visibility=0.0) for _ in range(33)]
    for index in (23, 25, 27):
        points[index] = SimpleNamespace(x=0.25, y=0.75, visibility=0.9)
    points[11] = SimpleNamespace(x=0.5, y=0.5, visibility=0.2)
    pose = SimpleNamespace(landmark=points)

    landmarks = extract_landmarks(pose, ("hip", "knee", "ankle"), (100, 200, 3))

    assert landmarks == {
        "hip": (50.0, 75.0),
        "knee": (50.0, 75.0),
        "ankle": (50.0, 75.0),
    }
