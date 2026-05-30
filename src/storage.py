from pathlib import Path
import json

BASE_DIR = Path.cwd().parent.parent

def save_raw_match(match_id: str, data: dict):
    path = BASE_DIR / "data" / "raw" / "matches" / f"{match_id}.json"

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return path
