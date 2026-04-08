from typing import Dict, Any, List

class TaskManager:
    """Manages the dataset and scenarios for our three tasks."""
    
    @staticmethod
    def get_easy_tasks() -> List[Dict[str, Any]]:
        return [
            {
                "id": "easy_1",
                "observation": {
                    "student_id": "student_1",
                    "eye_gaze": "looking away from screen, frequent glances at phone",
                    "posture": "slouched, chin resting on hand",
                    "facial_expression": "neutral to bored, occasional yawning",
                    "activity": "no notes taken in last 5 minutes, browser tab switched twice"
                },
                "ground_truth": "Disengaged"
            },
            {
                "id": "easy_2",
                "observation": {
                    "student_id": "student_2",
                    "eye_gaze": "focused on the main speaker",
                    "posture": "upright, leaning slightly forward",
                    "facial_expression": "attentive, occasional nodding",
                    "activity": "actively typing notes on the subject"
                },
                "ground_truth": "Engaged"
            }
        ]

    @staticmethod
    def get_medium_tasks() -> List[Dict[str, Any]]:
        return [
            {
                "id": "medium_1",
                "observation": [
                    {
                        "student_id": "std_10",
                        "eye_gaze": "focused on screen",
                        "posture": "upright",
                        "facial_expression": "attentive",
                        "activity": "typing"
                    },
                    {
                        "student_id": "std_11",
                        "eye_gaze": "staring blankly off-screen",
                        "posture": "slumping heavily",
                        "facial_expression": "drowsy",
                        "activity": "idle for 10 mins"
                    },
                    {
                        "student_id": "std_12",
                        "eye_gaze": "looking at phone",
                        "posture": "leaning back",
                        "facial_expression": "smiling at phone",
                        "activity": "camera occasionally covered"
                    },
                    {
                        "student_id": "std_13",
                        "eye_gaze": "looking at presentation",
                        "posture": "normal",
                        "facial_expression": "neutral",
                        "activity": "listening"
                    },
                    {
                        "student_id": "std_14",
                        "eye_gaze": "mostly at screen",
                        "posture": "straight",
                        "facial_expression": "engaged",
                        "activity": "taking notes actively"
                    }
                ],
                "ground_truth_disengaged_ids": ["std_11", "std_12"]
            }
        ]

    @staticmethod
    def get_hard_tasks() -> List[Dict[str, Any]]:
        return [
            {
                "id": "hard_1",
                "sequence": [
                    {
                        "time": "T+0",
                        "observation": {
                            "eye_gaze": "focused",
                            "posture": "upright",
                            "facial_expression": "attentive"
                        }
                    },
                    {
                        "time": "T+5min",
                        "observation": {
                            "eye_gaze": "frequent glances away",
                            "posture": "leaning on hand",
                            "facial_expression": "tired"
                        }
                    },
                    {
                        "time": "T+10min",
                        "observation": {
                            "eye_gaze": "eyes closed half the time",
                            "posture": "slouched entirely",
                            "facial_expression": "yawning repeatedly"
                        }
                    }
                ],
                "ground_truth_prediction": "Disengaged"
            }
        ]
