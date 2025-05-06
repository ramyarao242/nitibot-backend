import random
import os
import json
from fastapi import APIRouter, HTTPException, Query
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.verse_loader import verses

router = APIRouter()

@router.get("/verse/random")
def get_random_verse():
    return random.choice(verses)
    
@router.get("/ask-top3")
def ask_top3(question: str = Query(..., description="Ask your question")):
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    question_embedding = model.encode([question])
    
    similarities = []
    for verse in verses:
        if "embedding" in verse:
            verse_embedding = np.array(verse["embedding"]).reshape(1, -1)
            score = cosine_similarity(question_embedding, verse_embedding)[0][0]
            similarities.append((score, verse))
    
    top3 = sorted(similarities, key=lambda x: x[0], reverse=True)[:3]
    response = [
        {
            "match_score": round(score, 4),
            "verse": verse
        } for score, verse in top3
    ]
    return response    
    
@router.get("/ask")
def ask_chanakya(question: str = Query(...)):
    #model = SentenceTransformer("all-MiniLM-L6-v2")
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
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
