import random
import os
import json
from fastapi import APIRouter, HTTPException
from app.verse_loader import verses

router = APIRouter()

@router.get("/verse/random")
def get_random_verse():
    return random.choice(verses)

@router.get("/ask")
def ask_chanakya(question: str):
    keywords = {
        "trust": ["trust", "betray", "friend", "loyal"],
        "strategy": ["plan", "secret", "deceive", "succeed"],
        "wisdom": ["wise", "intelligence", "fool"]
    }
    q = question.lower()
    matched = []

    for terms in keywords.values():
        if any(term in q for term in terms):
            for v in verses:
                if any(term in v["translation"].lower() for term in terms):
                    matched.append(v)

    return random.choice(matched) if matched else random.choice(verses)

@router.get("/merge")
def merge_verses():
    directory = "./data"
    all_verses = []

    for chapter_num in range(1, 18):
        filename = f"Chapter{chapter_num}"
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_verses.extend(data)
        else:
            raise HTTPException(status_code=404, detail=f"{filename} not found")

    output_path = os.path.join(directory, "allChapters.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_verses, f, ensure_ascii=False, indent=2)

    return {
        "message": "Merged successfully",
        "total_verses": len(all_verses),
        "output_file": output_path
    }
