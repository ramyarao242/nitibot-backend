from fastapi import FastAPI, Query
from app.routes import get_random_verse, ask_chanakya,router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to NitiBot API"}

@app.get("/verse/random")
def verse_random():
    return get_random_verse()

@app.get("/verse/ask")
def verse_ask(question: str = Query(..., description="Your question to Chanakya")):
    return ask_chanakya(question)

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8020))  # this line is CRUCIAL
    uvicorn.run("main:app", host="0.0.0.0", port=port)
