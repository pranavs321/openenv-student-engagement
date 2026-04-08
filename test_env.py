from env.environment import StudentEngagementEnvironment, Action

def run_test():
    print("==== ACTIVATING OPENENV TEST ARENA ====\n")
    env = StudentEngagementEnvironment()
    
    # Task 1
    obs = env.reset()
    print("🟢 LEVEL 1: EASY TASK")
    print(f"Data feeding into AI: {obs.data}")
    # We mock the AI saying "Disengaged"
    action = Action(action_type="mock", payload={"label": "Disengaged"})
    obs, reward, done, info = env.step(action)
    print(f"Mock AI Answered: 'Disengaged'")
    print(f"Grader Score: {reward} / 1.0\n")
    
    # Task 2
    print("🟡 LEVEL 2: MEDIUM TASK")
    print(f"Data feeding into AI: [Classroom of 5 students...]")
    # We mock the AI finding one disengaged student and providing an intervention
    action = Action(action_type="mock", payload={"disengaged_student_ids": ["std_11"], "intervention": "Ask student 11 a direct question to wake them up."})
    obs, reward, done, info = env.step(action)
    print(f"Mock AI Answered: Identified 'std_11' and suggested an intervention.")
    print(f"Grader Score: {reward} / 1.0 (Partial credit! It missed student 12)\n")
    
    # Task 3
    print("🔴 LEVEL 3: HARD TASK")
    print(f"Data feeding into AI: {obs.data}")
    # We mock the AI predicting disengaged with reasoning
    action = Action(action_type="mock", payload={"prediction": "Disengaged", "reasoning": "The student has been actively slouching and closing their eyes over the 15 min trajectory."})
    obs, reward, done, info = env.step(action)
    print(f"Mock AI Answered: Predicted 'Disengaged' with strong logic.")
    print(f"Grader Score: {reward} / 1.0\n")
    
    print(f"✅ EXAM COMPLETE? {done}")

if __name__ == "__main__":
    run_test()
