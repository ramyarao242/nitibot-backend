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

@app.get('/merge', methods=['GET'])
def merge_verses():
    directory = "./app/data"
    all_verses = []

    for chapter_num in range(1, 18):
        filename = f"Chapter{chapter_num}.json"
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                chapter_data = json.load(f)
                all_verses.extend(chapter_data)
        except FileNotFoundError:
            return jsonify({"error": f"{filename} not found"}), 400

    output_path = os.path.join(directory, "chanakya_neeti_all_chapters.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_verses, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "Merged successfully", "total_verses": len(all_verses)}), 200
