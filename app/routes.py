import random
from app.verse_loader import verses

def get_random_verse():
    return random.choice(verses)

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


@routes.route('/merge', methods=['GET'])
def merge_verses():
    directory = "./data"
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
