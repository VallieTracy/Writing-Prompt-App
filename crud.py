"""CRUD operations"""

from model import db, User, Nugget, Word, connect_to_db

import random
import data.prompts as dp
import json



def create_user(email, first_name, last_name, password):
    """Create and return a new user."""

    user = User(email=email, first_name=first_name, last_name=last_name, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_nugget(nugget, email):
    """Create and return a new nugget"""

    nugget = Nugget(nugget=nugget, email=email)

    db.session.add(nugget)
    db.session.commit()

    return nugget

def create_word(word, email):
    """Create and return a new word"""    

    word = Word(word=word, email=email)

    db.session.add(word)
    db.session.commit()

    return word

def get_user_by_email(email):
    """Return a user object by email."""

    return User.query.filter(User.email == email).first()

def get_nuggets_by_email(email):
    """Return all nuggets by user email """

    nuggets = []
    
    for nugget in (Nugget.query.filter_by(email=email).all()):
        nuggets.append(nugget.nugget)
    
    return nuggets

def get_words_by_email(email):
    words = []
    for word in (Word.query.filter_by(email=email).all()):
        words.append(word.word)
    return words

def get_random_word():
    """Select random word from 'words' table"""

    return random.choice((Word.query.all())).word

def get_unique_second_word(word):
    """Select a unique second random word"""
    
    available_words = db.session.query(Word).filter(Word.word != word)
    # available_words = db.session.query(Word).filter(db.not_(Word.word.in_(used_words)))
    return random.choice((available_words.all())).word
    #Word.word not in used_words - put sqlalchemy syntax, something that isn't in a list

def get_unique_word(arr):
    available_words = db.session.query(Word).filter(db.not_(Word.word.in_(arr)))
    word = random.choice((available_words.all())).word
    return word

def get_all_words():

    all_words = Word.query.all()
    words_list = []
    for word in all_words:
        words_list.append(word.word)
    return words_list

def seed_words():
    with open('data/words.json') as f:
        word_data = json.loads(f.read())

    word_data = [word.lower() for word in word_data]
    current_db = [word.lower() for word in get_all_words()]
    
    for word in word_data:
        if word not in current_db:
            create_word(word, email=None)

def count_table():
    count = Word.query.count()
    return count


            
        
            


if __name__ == '__main__':
    from server import app
    connect_to_db(app)