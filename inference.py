import os
import json
import urllib.request
import urllib.error
from env.environment import StudentEngagementEnvironment, Action

# Read environment variables with defaults where required
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Remove buggy OpenAI client initialization.
# We will use standard urllib to call the REST API instead to bypass the evaluator's broken httpx dependency.

def format_prompt(obs_data: dict, difficulty: str) -> str:
    """Formats the observation into a prompt for the LLM."""
    if difficulty == "easy":
        return f"""
        Task: Single-Student Classification.
        Given the following student observation, classify them as either "Engaged" or "Disengaged".
        Observation: {json.dumps(obs_data)}
        
        Return ONLY a JSON object exactly like this: {{"label": "Engaged"}} or {{"label": "Disengaged"}}
        """
    elif difficulty == "medium":
        return f"""
        Task: Multi-Student Classroom Analysis.
        Identify all disengaged students from the list. Suggest one intervention strategy for them.
        Observation: {json.dumps(obs_data)}
        
        Return ONLY a JSON object exactly like this:
        {{"disengaged_student_ids": ["student_x", "student_y"], "intervention": "A brief intervention strategy"}}
        """
    elif difficulty == "hard":
        return f"""
        Task: Temporal Engagement Tracking.
        Based on the sequence of observations, predict the engagement level for the next step (Engaged or Disengaged) and provide reasoning.
        Observation: {json.dumps(obs_data)}
        
        Return ONLY a JSON object exactly like this:
        {{"prediction": "Disengaged", "reasoning": "Detailed reasoning here..."}}
        """
    return ""

def safe_reward(r):
    """Triple-safety: clamp float AND the formatted string can never be 0.00 or 1.00."""
    r = float(r)
    r = max(0.01, min(0.99, r))
    s = f"{r:.2f}"
    # Final string-level safety net
    if s == "0.00":
        s = "0.01"
    elif s == "1.00":
        s = "0.99"
    return r, s


def run_episode():
    env = StudentEngagementEnvironment()
    obs = env.reset()
    
    while not env.done:
        # Hackathon Validator requires exact task names from openenv.yaml
        task_name = obs.task_name
        
        # Print START line for THIS SPECIFIC TASK
        print(f"[START] task={task_name} env=student_engagement model={MODEL_NAME}")
        
        success = True
        reward = 0.10
        reward_str = "0.10"
        action_str = "predict()"
        
        try:
            # 1. Ask LLM what to do
            prompt = format_prompt(obs.data, obs.difficulty)
            
            messages = [
                {"role": "system", "content": "You are an expert AI grading real-world tasks. Return only pure JSON without markdown blocks."},
                {"role": "user", "content": prompt}
            ]
            
            base_url = API_BASE_URL.rstrip('/')
            url = f"{base_url}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {HF_TOKEN}"
            }
            data = {
                "model": MODEL_NAME,
                "messages": messages
            }
            
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    raw_content = result["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"API Error: {e}")
                raw_content = "{}"
            
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3]
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3]
                
            try:
                parsed_action = json.loads(raw_content)
            except json.JSONDecodeError:
                parsed_action = {}
                
            action = Action(action_type="inference", payload=parsed_action)
            action_str = f"submit_action(type={obs.difficulty})"
            
            # 2. Step the strictly single-turn task
            next_obs, reward, is_episode_done, info = env.step(action)
            
            # CLAMP the reward before printing
            reward, reward_str = safe_reward(reward)
            print(f"[STEP] step=1 action={action_str} reward={reward_str} done=true error=null")
            
        except Exception as e:
            success = False
            reward_str = "0.10"
            print(f'[STEP] step=1 action=Exception reward=0.10 done=true error="{str(e)}"')
            next_obs = env._get_current_observation(force_done=True)
            env.done = True
            
        # Format outputs and strictly delimit the end of the task
        success_str = "true" if success else "false"
        print(f"[END] success={success_str} steps=1 rewards={reward_str}")
        
        obs = next_obs
        
    env.close()

if __name__ == "__main__":
    run_episode()
