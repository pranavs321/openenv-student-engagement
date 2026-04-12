from typing import Any, Dict


def _clamp(score: float) -> float:
    """Guarantee score is strictly between 0 and 1 (not 0.0, not 1.0)."""
    return max(0.01, min(0.99, float(score)))


class BaseGrader:
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        raise NotImplementedError


class EasyGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        pred_label = ""
        if isinstance(action, dict):
            pred_label = action.get("label", "").lower()
        else:
            try:
                pred_label = action.label.lower()
            except AttributeError:
                pass

        gt = task_data["ground_truth"].lower()

        raw = 0.9 if gt in pred_label else 0.1
        return _clamp(raw)


class MediumGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        try:
            if isinstance(action, dict):
                pred_ids = action.get("disengaged_student_ids", [])
                intervention = action.get("intervention", "")
            else:
                pred_ids = action.disengaged_student_ids
                intervention = action.intervention
        except AttributeError:
            return _clamp(0.1)

        gt_ids = set(task_data["ground_truth_disengaged_ids"])
        pred_ids_set = set(pred_ids)

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


class HardGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        try:
            if isinstance(action, dict):
                pred = action.get("prediction", "").lower()
                reasoning = action.get("reasoning", "")
            else:
                pred = action.prediction.lower()
                reasoning = action.reasoning
        except AttributeError:
            return _clamp(0.1)

        gt_pred = task_data["ground_truth_prediction"].lower()

        pred_score = 0.9 if gt_pred in pred else 0.1
        reasoning_score = 0.9 if isinstance(reasoning, str) and len(reasoning.strip()) > 20 else 0.1

        final_score = (0.5 * pred_score) + (0.5 * reasoning_score)
        return _clamp(final_score)
