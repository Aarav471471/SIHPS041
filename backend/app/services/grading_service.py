import json
import os
from typing import List, Dict

CONTENT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "content")

def load_answer_key(module_code: str) -> Dict:
    path = os.path.join(CONTENT_PATH, "questions", f"{module_code}.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def grade_attempt(module_code: str, answers: List[dict], steps: List[dict]) -> dict:
    answer_key = load_answer_key(module_code)
    # grade answers
    assess_score = 100
    ar_score = 100
    
    # Very basic grading logic for now:
    correct_count = sum(1 for a in answers if a.get("is_correct"))
    if len(answers) > 0:
        assess_score = (correct_count / len(answers)) * 100
        
    pts = sum(s.get("points", 0) for s in steps)
    max_pts = sum(s.get("max_points", 0) for s in steps)
    if max_pts > 0:
        ar_score = (pts / max_pts) * 100
        
    final_score = (0.6 * assess_score) + (0.4 * ar_score)
    pass_mark = int(os.getenv("PASS_MARK", "70"))
    
    return {
        "assess_score": assess_score,
        "ar_score": ar_score,
        "server_score": final_score,
        "passed": final_score >= pass_mark
    }
