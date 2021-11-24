from unittest import TestCase
from server import app
from model import test_connect_to_db, db, example_data
from flask import session
import server

class FlaskTestsBasic(TestCase):
    """Flask tests"""

    def setUp(self):
        """Stuff to do before every test"""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage route"""

        result = self.client.get('/')
        self.assertIn(b"LOG IN", result.data)

    # don't need to do a tear down because the client closes on its own. DB does not do that.



class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        """Stuff to do before every test"""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        
        # Connect to test database
        test_connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test"""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login(self):
        """Test Login"""

        result = self.client.post('/start',
                                  data={'email': 'user@user', 'password': 'password'}, #needs to be a user in my example data!
                                  follow_redirects=True)
        self.assertIn(b"DIRECTIONS", result.data)

# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session"""

#     def setUp(self):
#         """Stuff to do before every test"""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

    

    

if __name__=="__main__":
    import unittest

    unittest.main()

# run createdb testdb in the terminal

    