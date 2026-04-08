import sys
from pathlib import Path

# Add the root directory to sys.path to allow importing from root app.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app, main

if __name__ == "__main__":
    main()
