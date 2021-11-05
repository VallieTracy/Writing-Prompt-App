"""CRUD operations"""

from model import db, User, Nugget, Word, connect_to_db

import random
import data.prompts as dp



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
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_random_word():
    """Select random word from 'words' table"""

    return random.choice((Word.query.all())).word

def get_unique_second_word():
    """Select a unique second random word"""
    
    available_words = db.session.query(Word).filter(Word.word != get_random_word())
    return random.choice((available_words.all())).word

if __name__ == '__main__':
    from server import app
    connect_to_db(app)