import json
from pathlib import Path

BANNED_WORD_FILE = Path("database/banned_words.json")

def load_banned_words():
    try:
        with open(BANNED_WORD_FILE,"r") as f:
            return json.load(f)
    except:
        return []

def save_banned_words(words):
    with open(BANNED_WORD_FILE,"w") as f:
        json.dump(words,f,indent=2)