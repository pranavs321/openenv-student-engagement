import yaml
import importlib
try:
    with open("openenv.yaml", "r") as f:
        config = yaml.safe_load(f)
    print(f"Tasks: {len(config.get('tasks', []))}")
    for t in config.get("tasks", []):
        grader_str = t.get("grader")
        mod_name, fn_name = grader_str.split(":")
        mod = importlib.import_module(mod_name)
        grader_fn = getattr(mod, fn_name)
        score1 = grader_fn("GARBAGE", {})
        score2 = grader_fn(None, None)
        score3 = grader_fn({"label": "Engaged"}, {"ground_truth": "Engaged"})
        print(f"[{t['id']}] Garbage: {score1}, None: {score2}, Engaged: {score3}")
        assert 0 < score1 < 1
        assert 0 < score2 < 1
        assert 0 < score3 < 1
except Exception as e:
    print(f"Failed! {e}")
