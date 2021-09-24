"""User model tests, pattern matching from Warbler Springboard project."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Photos, Favorites

# different db for tests

os.environ['DATABASE_URL'] = "postgresql:///moon-test"

#
# in each test, we'll need to delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()  # create and drop db

        # use signup method to create a user instance
        u1 = User.signup("HelloMello", "password")
        uid1 = 1111  # designate the uid to make referencing it easier
        u1.id = uid1

        # making another user copy
        u2 = User.signup("GoodMorningStarshine", "password")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()  # committing the user copies to the session

        u1 = User.query.get(uid1)  # establishing the variables
        u2 = User.query.get(uid2)

        self.u1 = u1  # storing all this info in self
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

# Does User.signup successfully create a new user given valid credentials?
    def test_valid_signup(self):
        # usimg signup method to create u to test against
        u_test = User.signup("test1", "password")
        uid = 99999  # creating an id
        u_test.id = uid  # assigning it to the u_test user
        db.session.commit()  # committing to session

        # fetching the test user from the session using uid
        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)  # testing that a value is there

        # testing that the username is the same as the test user's
        self.assertEqual(u_test.username, "test1")
        # testing that the password is the same as the test user's
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        # making sure the bcrypt strings are on the level
        self.assertTrue(u_test.password.startswith("$2b$"))

# Does User.signup fail to create a new user if the validations fail?
    def test_invalid_username_signup(self):
        # try to create user without username using signup method
        invalid = User.signup(None, "password")
        uid = 123456789  # creating id for invalid test user
        invalid.id = uid  # assigning the id to the invalid test user
        # use assertRaises to make sure the IntegrityError pops up
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()  # commit to session

    def test_invalid_password_signup(self):
        # make sure that when use signs up without entering pword a ValueError is raised
        with self.assertRaises(ValueError) as context:
            User.signup("test2", "")

# Does User.authenticate successfully return a user when given a valid username and password?
    def test_valid_authentication(self):
        # give a valid username/password
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)  # check user existence
        self.assertEqual(u.id, self.uid1)  # check u.id = u1 uid

# Does User.authenticate fail to return a user when the username is invalid?
    def test_invalid_username(self):
        # check that a bad username is assertedFalse
        self.assertFalse(User.authenticate("badusername", "password"))

# Does User.authenticate fail to return a user when the password is invalid?
    def test_wrong_password(self):
        # check that a bad pword is assertedFalse
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

# Does the basic model work?
    def test_user_model(self):

        u = User(
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no favorites yet
        self.assertEqual(len(u.favorites), 0)

    def tearDown(self):
        # calling super on teardown allows us to test more than one heirarchy multiple times
        res = super().tearDown()
        db.session.rollback()
        return res
