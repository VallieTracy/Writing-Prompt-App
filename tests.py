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
                                  data={'email': 'user@user', 'password': 'password'}, # needs to be a user in my example data!
                                  follow_redirects=True)
        self.assertIn(b"DIRECTIONS", result.data)

    def test_register(self):
        """Tests that after registration, the page redirects to the log-in page"""

        result = self.client.post('/register-user',
                                  data={'email': 'new_user@user', 'first_name': 'E', 'last_name': 'Tracy', 'password': 'password'}, # needs to be a user in my example data!
                                  follow_redirects=True)
        self.assertIn(b"LOG IN", result.data)

    def test_already_registered(self):
        """Tests that if a user tries to register with an email already in the db
        it will refresh the page"""

        result = self.client.post('/register-user',
                                  data={'email': 'user@user', 'first_name': 'SallyJoe', 'last_name': 'Tracy', 'password': 'new_password'}, # needs to be a user in my example data!
                                  follow_redirects=True)
        self.assertIn(b"Email:", result.data)

class FlaskTestsLogInLogOut(TestCase):
    """Test log-in and log-out"""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

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
        """Test log-in form"""

        with self.client as c:
            result = c.post('/start',
                            data={'email': 'user@user', 'first_name': 'Sally', 'last_name': None, 'password': 'password'},
                            follow_redirects=True
                            )
            self.assertEqual(session['first_name'], 'Sally')
            self.assertIn(b"DIRECTIONS", result.data)

    def test_logout(self):
        """Test logout session end"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['first_name'] = 'Sally'

            result = self.client.post('/logout', follow_redirects=True)

            self.assertNotIn(b'first_name', session)
            self.assertIn(b'B', result.data)

        



            


    

    

if __name__=="__main__":
    import unittest

    unittest.main()

# run createdb testdb in the terminal

    