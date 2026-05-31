from pathlib import Path
import logging
import json
import os

BASE_DIR = Path(__file__).parent.parent

def save_raw_match(match_id: str, data: dict):
    path = BASE_DIR / "data" / "raw" / "matches" / f"{match_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    
    os.makedirs("data/raw", exist_ok=True)

    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f"Raw data saved for match {match_id}, skipping.")
    else:
        logging.info(f"Raw data already exists for match {match_id}, skipping.")
        
        
    return path
