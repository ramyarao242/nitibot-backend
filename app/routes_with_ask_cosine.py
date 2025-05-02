from fastapi import APIRouter, Query
from app.verse_loader import verses
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

router = APIRouter()

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