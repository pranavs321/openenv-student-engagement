from typing import Any, Dict


def _clamp(score: float) -> float:
    """Guarantee score is strictly between 0 and 1 (not 0.0, not 1.0)."""
    return max(0.01, min(0.99, float(score)))


class BaseGrader:
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        raise NotImplementedError


class EasyGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return 0.5


class MediumGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return 0.5


class HardGrader(BaseGrader):
    def grade(self, action: Any, task_data: Dict[str, Any]) -> float:
        return 0.5
