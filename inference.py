import os
import json
from openai import OpenAI
from env.environment import StudentEngagementEnvironment, Action

# Read environment variables with defaults where required
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

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

def run_episode():
    env = StudentEngagementEnvironment()
    obs = env.reset()
    
    # Initialize trackers
    total_steps = 0
    all_rewards = []
    
    # Print START line
    print(f"[START] task=student_engagement env=openenv model={MODEL_NAME}")
    
    done = False
    success = True # Assume success unless an exception breaks the loop
    
    try:
        while not done:
            total_steps += 1
            
            # 1. Ask LLM what to do
            prompt = format_prompt(obs.data, obs.difficulty)
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert AI grading real-world tasks. Return only pure JSON without markdown blocks."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            raw_content = response.choices[0].message.content.strip()
            
            # Clean up potential markdown formatting (```json ... ```)
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3]
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3]
                
            try:
                parsed_action = json.loads(raw_content)
            except json.JSONDecodeError:
                # If LLM fails to output valid JSON, create a dummy action
                parsed_action = {}
                
            # Define action
            action = Action(action_type="inference", payload=parsed_action)
            
            # 2. Step the environment
            next_obs, reward, is_episode_done, info = env.step(action)
            all_rewards.append(reward)
            
            # Format outputs to 2 decimal places as requested
            reward_str = f"{reward:.2f}"
            done_str = "true" if is_episode_done else "false"
            action_str = "submit_classification()" if obs.difficulty == "easy" else "submit_analysis()"
            error_msg = "null"
            
            # Print STEP line
            print(f"[STEP] step={total_steps} action={action_str} reward={reward_str} done={done_str} error={error_msg}")
            
            obs = next_obs
            done = is_episode_done
            
    except Exception as e:
        success = False
        print(f"[STEP] step={total_steps} action=Exception reward=0.00 done=true error=\"{str(e)}\"")
    finally:
        env.close()
        
        # Format outputs
        success_str = "true" if success else "false"
        rewards_str = ",".join([f"{r:.2f}" for r in all_rewards])
        
        # Print END line
        print(f"[END] success={success_str} steps={total_steps} rewards={rewards_str}")

if __name__ == "__main__":
    run_episode()
