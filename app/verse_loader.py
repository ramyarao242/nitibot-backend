import json
import os
from sentence_transformers import SentenceTransformer

# Load all verses from merged JSON
file_path = os.path.abspath("app/data/chanakya_neeti_all_chapters.json")
with open(file_path, "r", encoding="utf-8") as f:
    verses = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate and store embeddings
for verse in verses:
    if "translation" in verse:
        verse["embedding"] = model.encode(verse["translation"]).tolist()
