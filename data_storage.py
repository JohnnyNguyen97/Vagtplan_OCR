import json
import os
from datetime import datetime

DATA_FILE = "shift_history.json"

def load_history():
    """Load existing shift history from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_shifts(shifts, salary_data):
    """Save shifts to JSON history with timestamp"""
    history = load_history()
    
    entry = {
        "date_saved": datetime.now().isoformat(),
        "shifts": shifts,
        "salary_data": salary_data
    }
    
    history.append(entry)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    return len(history)
