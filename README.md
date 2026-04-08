# Student Engagement Detection - OpenEnv Environment

This is a submission for the Meta OpenEnv Hackathon. This environment evaluates the capability of Large Language Models (LLMs) to accurately interpret multimodal cues (eye gaze, posture, facial expressions, general activity) representing student classroom behaviors, and correctly classify or predict their classroom engagement levels.

## Motivation
Measuring student engagement reliably requires fusing multiple signals accurately. AI agents capable of monitoring these behaviors and making real-time, logical inferences could revolutionize automated EdTech and virtual teaching assistants. 

## Action and Observation Spaces

### Observation Space
The environment emits observations as structured models describing a single student or a classroom of students, detailing:
- `eye_gaze`
- `posture`
- `facial_expression`
- `activity`

Observations also include the current `task_name` and task `difficulty`.

### Action Space
The Action generic implementation varies slightly by difficulty but expects the LLM to provide:
- **Easy:** `{ "label": "Engaged" | "Disengaged" }`
- **Medium:** `{ "disengaged_student_ids": ["id_1", ...], "intervention": "..." }`
- **Hard:** `{ "prediction": "Engaged" | "Disengaged", "reasoning": "..." }`

## Task Difficulty Levels

1. **🟡 Easy (Single-Student Classification)**: Analyze distinct behavioral signals and correctly classify a single student.
2. **🟠 Medium (Multi-Student Analysis)**: Evaluate 5 simultaneous student descriptions, identify all disengagements, and recommend a strategy.
3. **🔴 Hard (Temporal Engagement Tracking)**: Follow a student's trajectory over multiple timestamps, extrapolate the trend, and determine the incoming future state with sound reasoning.

## Execution and Evaluation Structure

In adherence to the OpenEnv guidelines, this project follows the primary specification:
- Dockerized for Hugging Face (complies with 2 vCPU and 8 GB constraint).
- Contains standard `openenv.yaml` specification.
- Executes via `inference.py` script locally on the root, reading `HF_TOKEN`, `MODEL_NAME`, and `API_BASE_URL`.
- Implements standard OpenEnv methods (`reset`, `step`, `state`, `close`).
- Outputs standard `[START]`, `[STEP]`, `[END]` evaluation logs explicitly aligned with requirements.

## How to Run

1. Make sure required dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Export your Hugging Face API key (used as OpenAI proxy key for the Hackathon platform):
   ```bash
   export HF_TOKEN="your_hugging_face_token_here"
   export MODEL_NAME="gpt-4.1-mini"  # Or your chosen model for testing
   ```
3. Run the evaluation baseline:
   ```bash
   python inference.py
   ```
