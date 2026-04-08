import sys
import uvicorn
from pathlib import Path

# Add the root directory to Python path to allow importing from root app.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app

def main():
    import os
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
