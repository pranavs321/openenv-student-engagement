from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import uvicorn
from env.environment import StudentEngagementEnvironment, Action

app = FastAPI()

# Create a global instance of your environment so the server can play it!
open_env = StudentEngagementEnvironment()

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "openenv-student-engagement"}

# The exact endpoints the Hackathon Portal robot is looking for!
@app.post("/reset")
def reset():
    obs = open_env.reset()
    return {"observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict()}

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = open_env.step(action)
    return {
        "observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return open_env.state()

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
