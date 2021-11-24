from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

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

# class FlaskTestsDatabase(TestCase):
#     """Flask tests that use the database"""

#     def setUp(self):
#         """Stuff to do before every test"""

#         # Get the Flask test client
#         self.client = app.test_client()
#         app.config['TESTING'] = True
        
#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """Do at end of every test"""

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()

if __name__=="__main__":
    import unittest

    unittest.main()

    