from typing import Any, Dict

class BaseGrader:
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        raise NotImplementedError

class EasyGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        # action is expected to be a string or a dict containing 'label'
        # we will handle parsing from the action models defined in environment.py
        pred_label = ""
        if isinstance(action, dict):
            pred_label = action.get("label", "").lower()
        else:
            try:
                pred_label = action.label.lower()
            except AttributeError:
                pass
        
        gt = task_data["ground_truth"].lower()
        
        if gt in pred_label:
            return 0.99
        return 0.01

class MediumGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        # action is expected to have disengaged_student_ids (List[str]) and intervention (str)
        try:
            if isinstance(action, dict):
                pred_ids = action.get("disengaged_student_ids", [])
                intervention = action.get("intervention", "")
            else:
                pred_ids = action.disengaged_student_ids
                intervention = action.intervention
        except AttributeError:
            return 0.01

        gt_ids = set(task_data["ground_truth_disengaged_ids"])
        pred_ids_set = set(pred_ids)

        if not gt_ids and not pred_ids_set:
            accuracy_score = 0.99
        else:
            intersection = gt_ids.intersection(pred_ids_set)
            union = gt_ids.union(pred_ids_set)
            accuracy_score = len(intersection) / len(union) if union else 0.01

        intervention_score = 0.01
        if isinstance(intervention, str) and len(intervention.strip()) > 10:
            intervention_score = 0.99
            
        # 60% accuracy on ID picking, 40% on providing a valid non-empty intervention
        final_score = (0.6 * accuracy_score) + (0.4 * intervention_score)
        return float(final_score)

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
            return 0.01
            
        gt_pred = task_data["ground_truth_prediction"].lower()
        
        pred_score = 0.99 if gt_pred in pred else 0.01
        reasoning_score = 0.99 if isinstance(reasoning, str) and len(reasoning.strip()) > 20 else 0.01
        
        # 50% for correct prediction, 50% for providing adequate reasoning
        return float((0.5 * pred_score) + (0.5 * reasoning_score))
