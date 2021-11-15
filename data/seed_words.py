import json

def seed_words():
    with open('words.json') as f:
        word_data = json.loads(f.read())
    return word_data