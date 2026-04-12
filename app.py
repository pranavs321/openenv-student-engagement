from fastapi import FastAPI, Body
from typing import Any, Dict
import uvicorn
from env.environment import StudentEngagementEnvironment, Action
from env.graders import _clamp

app = FastAPI()

# Create a global instance of your environment
open_env = StudentEngagementEnvironment()

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "openenv-student-engagement"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Match openenv-core HTTPEnvServer format EXACTLY
@app.post("/reset")
async def reset(request: Dict[str, Any] = Body(default={})):
    obs = open_env.reset()
    obs_dict = obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict()
    return {
        "observation": obs_dict,
        "reward": None,
        "done": False,
        "info": {},
    }

@app.post("/step")
async def step(request: Dict[str, Any] = Body(default={})):
    # openenv-core sends {"action": {...}} format
    action_data = request.get("action", request)
    
    # Build Action object from whatever the validator sends
    if isinstance(action_data, dict):
        action_obj = Action(action_type="inference", payload=action_data)
    else:
        action_obj = Action(action_type="inference", payload={})
    
    obs, reward, done, info = open_env.step(action_obj)
    
    # ALWAYS clamp the reward to be strictly between 0 and 1
    reward = _clamp(float(reward))
    
    obs_dict = obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict()
    return {
        "observation": obs_dict,
        "reward": reward,
        "done": done,
        "info": info,
    }

@app.get("/state")
def state():
    s = open_env.state()
    return s.model_dump() if hasattr(s, 'model_dump') else s.dict()

@app.post("/close")
def close():
    open_env.close()
    return {"status": "closed"}

def main():
    import os
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
