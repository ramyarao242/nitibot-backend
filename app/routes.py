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