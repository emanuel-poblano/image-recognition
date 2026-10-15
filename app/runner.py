"""Frame-processing loop shared by the live app and the evaluation harness."""

from analysis.landmarks import extract_landmarks
from analysis.session import Session
from exercises import EXERCISES

REQUIRED = {"squat": ("hip", "knee", "ankle"), "pushup": ("shoulder", "elbow", "wrist")}


def process_frames(frames, pose, exercise_name, on_frame=None, session=None):
    """Run pose + exercise tracking over frames. Frames without a reliable
    pose are skipped (counted in tracking_rate), never fed to the counter."""
    if session is None:
        exercise = EXERCISES[exercise_name]()
        session = Session(exercise)
    else:
        exercise = session.exercise
    feedback = "No person detected"
    for frame in frames:
        pl = pose.process_frame(frame)
        lm = extract_landmarks(pl, REQUIRED[exercise_name], frame.shape)
        if lm is None:
            feedback = "Body not fully visible"
            session.update(False)
        else:
            feedback, _ = exercise.analyze(lm)
            session.update(True, feedback)
        if on_frame is not None and on_frame(frame, pl, feedback, exercise.reps) is False:
            break
    return exercise, session
