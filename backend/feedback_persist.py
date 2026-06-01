"""
Feedback persistence layer - saves to JSON file + auto-commits to git.
This ensures feedback data survives Render redeployments.
"""
import json
import os
import subprocess
from datetime import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback_data.json")
REPO_DIR = os.path.dirname(__file__)

def load_feedback_from_json():
    """Load feedback entries from JSON file. Returns list of dicts."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_feedback_to_json(entries):
    """Save feedback entries to JSON file."""
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def append_feedback(entry):
    """Append a single feedback entry and auto-commit to git."""
    entries = load_feedback_from_json()
    entries.append(entry)
    save_feedback_to_json(entries)
    try:
        auto_git_commit(f"feedback: new {entry.get('category','')} from {entry.get('name','anonymous')}")
    except Exception as e:
        print(f"Git auto-commit failed (non-fatal): {e}")

def auto_git_commit(message="auto: feedback data update"):
    """Auto-commit and push feedback data to git."""
    try:
        result = subprocess.run(
            ["git", "add", "feedback_data.json"],
            cwd=REPO_DIR,
            capture_output=True, text=True, timeout=30
        )
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_DIR,
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=REPO_DIR,
                capture_output=True, text=True, timeout=60
            )
            print(f"Feedback auto-pushed to git")
        else:
            print(f"Git commit skipped: {result.stdout[:100]}")
    except Exception as e:
        print(f"Git operation failed: {e}")

def seed_feedback_to_db(db):
    """On startup, load JSON feedback into DB if DB is empty."""
    from models import Feedback
    existing = db.query(Feedback).count()
    if existing > 0:
        print(f"DB has {existing} feedback entries, skipping JSON seed")
        return
    
    entries = load_feedback_from_json()
    if not entries:
        print("No JSON feedback data to seed")
        return
    
    for e in entries:
        fb = Feedback(
            name=e.get("name", "Anonymous"),
            role=e.get("role", ""),
            category=e.get("category", "suggestion"),
            content=e.get("content", ""),
        )
        db.add(fb)
    db.commit()
    print(f"Seeded {len(entries)} feedback entries from JSON to DB")
