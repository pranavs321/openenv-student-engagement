import re

logs = """
[START] task=single_student_classification env=student_engagement model=gpt-4.1-mini
[STEP] step=1 action=submit_action(type=easy) reward=0.50 done=true error=null
[END] success=true steps=1 rewards=0.50
"""

def extract_score(logs):
    # What would be the regex?
    match = re.search(r"score=([\d\.]+)", logs)
    if match: return float(match.group(1))
    match = re.search(r"reward=([\d\.]+).*\n\[END\]", logs)
    if match: return float(match.group(1))
    return 0.5

print(extract_score(logs))
