import sys
sys.path.append('.')
from env.graders import grade_easy, grade_medium, grade_hard

for name, fn in [("easy", grade_easy), ("medium", grade_medium), ("hard", grade_hard)]:
    score1 = fn("GARBAGE", {})
    score2 = fn(None, None)
    score3 = fn({"label": "Engaged"}, {"ground_truth": "Engaged"})
    print(f"[{name}] Garbage: {score1}, None: {score2}, Engaged: {score3}")
    assert 0 < score1 < 1
    assert 0 < score2 < 1
    assert 0 < score3 < 1
