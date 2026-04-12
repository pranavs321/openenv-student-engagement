from typing import Union, List, Dict, Any, Tuple
from pydantic import BaseModel
from .tasks import TaskManager
from .graders import EasyGrader, MediumGrader, HardGrader, _clamp

# ---- OpenEnv Typed Models ----

class Observation(BaseModel):
    task_name: str
    difficulty: str
    data: Any

class Action(BaseModel):
    # This is a generic action model. 
    # For a real robust environment, you might define union types or separate action models per task
    action_type: str
    payload: Dict[str, Any]

class Reward(BaseModel):
    value: float
    is_done: bool

class State(BaseModel):
    current_task_index: int
    total_tasks: int
    current_difficulty: str

# ---- Environment Implementation ----

class StudentEngagementEnvironment:
    """
    OpenEnv implementation for Student Engagement Detection.
    Iterates sequentially over easy, medium, and hard tasks.
    """
    def __init__(self):
        self.easy_tasks = TaskManager.get_easy_tasks()
        self.medium_tasks = TaskManager.get_medium_tasks()
        self.hard_tasks = TaskManager.get_hard_tasks()
        
        self.tasks = []
        for t in self.easy_tasks:
            self.tasks.append((t, "easy", EasyGrader()))
        for t in self.medium_tasks:
            self.tasks.append((t, "medium", MediumGrader()))
        for t in self.hard_tasks:
            self.tasks.append((t, "hard", HardGrader()))
            
        self.current_task_idx = 0
        self.done = False

    def reset(self) -> Observation:
        """Starts the environment and returns the first observation."""
        self.current_task_idx = 0
        self.done = False
        return self._get_current_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """Processes the action and returns the next state."""
        if self.done or self.current_task_idx >= len(self.tasks):
            # Environment is already done — return clamped float, NOT Reward object
            return self._get_current_observation(force_done=True), _clamp(0.1), True, {"error": "Environment has already completed all tasks."}

        current_task_data, difficulty, grader = self.tasks[self.current_task_idx]
        
        # Grade the action based on the specific grader
        try:
            score = grader.grade(action.payload, current_task_data)
        except Exception as e:
            score = 0.1
        
        # ALWAYS clamp the score to be strictly between 0 and 1
        score = _clamp(score)
            
        info = {"task_id": current_task_data["id"], "score": score}

        # Move to next task
        self.current_task_idx += 1
        is_episode_done = self.current_task_idx >= len(self.tasks)
        self.done = is_episode_done
        
        obs = self._get_current_observation(force_done=is_episode_done)
        
        # Return clamped float score directly — NOT a Reward object
        return obs, score, is_episode_done, info

    def state(self) -> State:
        """Returns the current internal state."""
        diff = "completed"
        if self.current_task_idx < len(self.tasks):
            _, diff, _ = self.tasks[self.current_task_idx]
            
        return State(
            current_task_index=self.current_task_idx,
            total_tasks=len(self.tasks),
            current_difficulty=diff
        )

    def close(self):
        """Cleanup, if any."""
        pass

    def _get_current_observation(self, force_done=False) -> Observation:
        if force_done or self.current_task_idx >= len(self.tasks):
            return Observation(task_name="Done", difficulty="none", data={})
            
        task_data, difficulty, _ = self.tasks[self.current_task_idx]
        
        # Filter out ground truth from observation!
        obs_data = task_data.get("observation", task_data.get("sequence", {}))
        
        return Observation(
            task_name=task_data["id"],
            difficulty=difficulty,
            data=obs_data
        )
