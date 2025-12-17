from analysis.angles import calculate_angle

def test_right_angle():
    assert calculate_angle((0,1),(0,0),(1,0)) == 90
