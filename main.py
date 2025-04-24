from fastapi import FastAPI, Query
from app.routes import get_random_verse, ask_chanakya

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to NitiBot API"}

@app.get("/verse/random")
def verse_random():
    return get_random_verse()

@app.get("/verse/ask")
def verse_ask(question: str = Query(..., description="Your question to Chanakya")):
    return ask_chanakya(question)