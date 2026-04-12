"""Lightweight package exports.

Keep grader imports dependency-free so external validators can import
`env.graders:*` without needing the full environment stack.
"""

from .graders import BaseGrader, EasyGrader, MediumGrader, HardGrader

try:
    from .environment import StudentEngagementEnvironment
    from .tasks import TaskManager
except Exception:
    StudentEngagementEnvironment = None
    TaskManager = None

__all__ = [
    "StudentEngagementEnvironment",
    "TaskManager",
    "BaseGrader",
    "EasyGrader",
    "MediumGrader",
    "HardGrader",
]
