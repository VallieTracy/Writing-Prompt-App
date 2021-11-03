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

# BELOW HERE: This is relating to my prompts.py file, so I'm thinking I should put this in another file.  CRUD only for db stuff??
def test():

    prompts_list = dp.prompts_dicts
    for dictionary in prompts_list:
        print(dictionary['directions'])
    

    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)