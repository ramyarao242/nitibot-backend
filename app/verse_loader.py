import json
from pathlib import Path

def load_verses():
    path = Path("app/data/chanakya_neeti_sample.json")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

verses = load_verses()