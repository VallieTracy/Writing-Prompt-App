"""Setting up classes for my database and tables"""
# DB name - writers

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    email = db.Column(db.String, unique=True, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30))
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User first_name = {self.first_name}; email = {self.email}>'



class Nugget(db.Model):
    """A nugget of writing that the user would like to store"""

    __tablename__ = 'nuggets'

    nugget_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nugget = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)

    user = db.relationship('User', backref='nuggets')

    def __repr__(self):
        return f'<Nugget nugget_id = {self.nugget_id}; email = {self.email}; nugget = {self.nugget}>'

class Word(db.Model):
    """A list of words for the writing prompts.  Will be attached to an email if a user has added it.  Otherwise it's considered part of the original 2,500 words"""

    __tablename__ = 'words'

    word = db.Column(db.String(100), primary_key=True, unique=True)
    email = db.Column(db.String, db.ForeignKey('users.email'), nullable=True)

    user = db.relationship('User', backref='words')

    def __repr__(self):
        return f'<Word word = {self.word}; email = {self.email}>'

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Nugget.query.delete()
    Word.query.delete()

    # Add sample users, nuggets, and words
    user1 = User(email='user@user', first_name='Sally', last_name=None, password='password')
    user2 = User(email='me@me.com', first_name='Me', last_name='notme', password='password')

    nugget1 = Nugget(nugget='This is a nugget', email='user@user')
    nugget2 = Nugget(nugget='This is a second nugget', email='me@me.com')

    word1 = Word(word='bush', email='user@user')
    word2 = Word(word='two', email='user@user')

    db.session.add_all([user1, user2, nugget1, nugget2, word1, word2])
    db.session.commit()

def connect_to_db(flask_app, db_uri="postgresql:///writers", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

def test_connect_to_db(flask_app, db_uri="postgresql:///testdb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the test db!")


if __name__ == "__main__": #does something so we can use our application
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)