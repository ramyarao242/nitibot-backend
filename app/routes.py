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
def ask_chanakya(question: str = Query(...)):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    q_embedding = model.encode(question)

    best_score = -1
    best_verse = None

    for verse in verses:
        sim = cosine_similarity([q_embedding], [verse["embedding"]])[0][0]
        if sim > best_score:
            best_score = sim
            best_verse = verse

    return {
        "match_score": round(best_score, 4),
        "verse": best_verse
    }

@router.get("/merge")
def merge_verses():
    directory = "./app/data"
    all_verses = []

    for chapter_num in range(1, 18):
        filename = f"Chapter{chapter_num}"  # <-- no .json here
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_verses.extend(data)
        else:
            raise HTTPException(status_code=404, detail=f"{filename} not found")

    output_file = os.path.join(directory, "chanakya_neeti_all_chapters.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_verses, f, ensure_ascii=False, indent=2)

    return {
        "message": "Merged successfully",
        "total_verses": len(all_verses),
        "output_file": output_file
    } 

from fastapi.responses import FileResponse
import os

@router.get("/download")
def download_merged_file():
    file_path = os.path.abspath("app/data/chanakya_neeti_all_chapters.json")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="chanakya_neeti_all_chapters.json",
            media_type="application/json"
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")
