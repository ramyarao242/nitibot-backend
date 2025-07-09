import random
import os
import json
from fastapi import APIRouter, HTTPException, Query
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.verse_loader import verses
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
load_dotenv()  # Load environment variables from .env fil
#openai.api_key = os.getenv("OPENAI_API_KEY");

router = APIRouter()

@router.get("/verse/random")
def get_random_verse():
    return random.choice(verses)

@router.get("/verse/all-verses")
def get_all_verses():
    return verses

@router.get("/ask-top4")
def ask_top4(question: str = Query(..., description="Ask your question")):
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    question_embedding = model.encode([question])
    
    similarities = []
    for verse in verses:
        if "embedding" in verse:
            verse_embedding = np.array(verse["embedding"]).reshape(1, -1)
            score = cosine_similarity(question_embedding, verse_embedding)[0][0]
            similarities.append((score, verse))
    
    top3 = sorted(similarities, key=lambda x: x[0], reverse=True)[:4]
    response = [
        {
            "match_score": round(score, 4),
            "chapter": verse.get("chapter"),
            "verse": verse.get("verse"),
            "sanskrit": verse.get("sanskrit"),
            "translation": verse.get("translation"),
        } for score, verse in top3
    ]
    return response   

@router.get("/ask-chanakya")
def ask_chanakya(question: str = Query(...)):
    if not question:
        raise HTTPException(status_code=400, detail="Question parameter is required")
    prompt=( f"You are a wise sage named Chanakya. "
             f"Answer the question based on the wisdom of Chanakya Neeti with stratergic wisdom."
             f"Question: {question}"
             f"Verses:\n"+"\n".join(verses))
    # Call OpenAI API to get the response
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a wise sage named Chanakya, answering with sharp Neeti wisdom"},
                {"role": "user", "content": prompt}
            ], 
            temperature=0.7,
        )

        answer = response.choices[0].message.content
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

    return response

@router.get("/ask")
def ask_model(question: str = Query(...)):
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
    
@router.get("/daily-challenge")
def daily_challenge():
    prompt = (
    "Generate a strategic dilemma inspired by Chanakya Neeti. "
    "Respond in the following JSON format only:\n\n"
    "{\n"
    "  \"scenario\": \"<short moral or political dilemma>\",\n"
    "  \"options\": [\n"
    "    {\"text\": \"<Option A>\", \"score\": <1–10>},\n"
    "    {\"text\": \"<Option B>\", \"score\": <1–10>},\n"
    "    {\"text\": \"<Option C>\", \"score\": <1–10>},\n"
    "    {\"text\": \"<Option D>\", \"score\": <1–10>}\n"
    "  ],\n"
    "  \"takeaway\": \"<A strategic lesson related to the best option>\"\n"
    "}\n\n"
    "Ensure:\n"
    "- Options reflect realistic moral or strategic choices\n"
    "- Only one option should clearly have the highest score (like 9 or 10)\n"
    "- Scores reflect the wisdom behind each option\n"
    "- The takeaway must be aligned with the best option"
)
    # Call OpenAI API to get the response
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a wise sage Chanakya, Share daily stratergic dilemmas with sharp insights"},
                {"role": "user", "content": prompt}
            ], 
            temperature=0.7,
        )

        content = response.choices[0].message.content
        return JSONResponse(content={"challenge": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
