"""CRUD operations"""

from model import db, User, Nugget, connect_to_db

def create_user(email,first_name, last_name, password):
    """Create and return a new user."""

    user = User(email=email, first_name=first_name, last_name=last_name, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_nugget()






if __name__ == '__main__':
    from server import app
    connect_to_db(app)