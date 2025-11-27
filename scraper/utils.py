import json
import os


def load_hash_db(filepath: str) -> dict:
    """Load hash database from JSON file."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hash_db(filepath: str, data: dict) -> None:
    """Save hash database to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
