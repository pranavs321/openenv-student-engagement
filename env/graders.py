from typing import Any, Dict
import math

def _clamp(score: float) -> float:
    """Guarantee score stays safely inside (0, 1) even after rounding."""
    try:
        score = float(score)
    except (ValueError, TypeError):
        score = 0.5
    if not math.isfinite(score):
        score = 0.5
    # Keep values in a safe interior band to avoid validator-side rounding to 0.0/1.0.
    clamped = max(0.1, min(0.9, score))
    # Final safety: if it somehow rounds to 0 or 1, force to middle
    if clamped <= 0.0 or clamped >= 1.0:
        clamped = 0.5
    return clamped

def grade_easy(action: Any, task_data: Dict[str, Any]) -> float:
    try:
        pred_label = ""
        if isinstance(action, dict):
            pred_label = str(action.get("label", "")).lower()
        else:
            try:
                pred_label = str(action.label).lower()
            except AttributeError:
                pass

        if not isinstance(task_data, dict):
            return _clamp(0.1)

        gt = str(task_data.get("ground_truth", "")).lower()
        raw = 0.9 if gt in pred_label else 0.1
        return _clamp(raw)
    except Exception as e:
        return _clamp(0.5)

def grade_medium(action: Any, task_data: Dict[str, Any]) -> float:
    try:
        pred_ids = []
        intervention = ""
        if isinstance(action, dict):
            pred_ids = action.get("disengaged_student_ids", [])
            intervention = action.get("intervention", "")
        else:
            try:
                pred_ids = action.disengaged_student_ids
                intervention = action.intervention
            except AttributeError:
                pass

        if not isinstance(task_data, dict):
            return _clamp(0.1)

        gt_ids = task_data.get("ground_truth_disengaged_ids", [])
        if not isinstance(gt_ids, (list, set, tuple)):
            gt_ids = []
        gt_ids = set(str(x) for x in gt_ids)

        if not isinstance(pred_ids, (list, set, tuple)):
            pred_ids = []
        pred_ids_set = set(str(x) for x in pred_ids)

        if not gt_ids and not pred_ids_set:
            accuracy_score = 0.9
        else:
            intersection = gt_ids.intersection(pred_ids_set)
            union = gt_ids.union(pred_ids_set)
            ratio = len(intersection) / len(union) if union else 0.0
            accuracy_score = 0.1 + (ratio * 0.8)

        intervention_score = 0.1
        if isinstance(intervention, str) and len(intervention.strip()) > 10:
            intervention_score = 0.9

        final_score = (0.6 * accuracy_score) + (0.4 * intervention_score)
        return _clamp(final_score)
    except Exception as e:
        return _clamp(0.5)

def grade_hard(action: Any, task_data: Dict[str, Any]) -> float:
    try:
        pred = ""
        reasoning = ""
        if isinstance(action, dict):
            pred = str(action.get("prediction", "")).lower()
            reasoning = str(action.get("reasoning", ""))
        else:
            try:
                pred = str(action.prediction).lower()
                reasoning = str(action.reasoning)
            except AttributeError:
                pass

        if not isinstance(task_data, dict):
            return _clamp(0.1)

        gt_pred = str(task_data.get("ground_truth_prediction", "")).lower()

        pred_score = 0.9 if gt_pred in pred else 0.1
        reasoning_score = 0.9 if len(reasoning.strip()) > 20 else 0.1

        final_score = (0.5 * pred_score) + (0.5 * reasoning_score)
        return _clamp(final_score)
    except Exception as e:
        return _clamp(0.5)

# For backwards compatibility with env/environment.py which imports the classes
class BaseGrader:
    pass

class EasyGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return grade_easy(action, task_data)

class MediumGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return grade_medium(action, task_data)

class HardGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return grade_hard(action, task_data)
