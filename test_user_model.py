"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follow, DEFAULT_IMAGE_URL, DEFAULT_HEADER_IMAGE_URL

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
app.config['TESTING'] = True

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
FLASK_DEBUG = False
# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test of User class and Follow class/ join table"""

    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Test to se if users have been properly instantiated"""

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u2.messages), 0)
        self.assertEqual(len(u2.followers), 0)
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)
        self.assertEqual(u1.header_image_url, DEFAULT_HEADER_IMAGE_URL)

    def test_follow(self):
        """ Test to see if u1 can follow u2
        and user instance methods is_followed_by & is_following """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)
        new_follow = Follow(user_being_followed_id=self.u1_id,
                            user_following_id=self.u2_id)
        db.session.add(new_follow)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))
        self.assertTrue(u2.is_following(u1))
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))

    def test_authenticate_success(self):
        """Testing class method authenticate() success"""

        self.assertIsInstance(User.authenticate(
            username="u1", password="password"), User)

    def test_authenticate_fail(self):
        """Testing class method authenticate() failer"""

        # Wrong username
        self.assertFalse(User.authenticate(
            username="wrong", password="password"))

        # Wrong password
        self.assertFalse(User.authenticate(username="u1", password="wrong"))

    def test_signup(self):
        """Check for new user signup"""

        good_test = User.signup(
            "good_test", "good_test@email.com", "password", None)
        db.session.add(good_test)
        db.session.commit()

        # Integrity Error test (Doctests don't allow for )

        # Test successful registration
        self.assertIsInstance(good_test, User)
        self.assertEqual(len(good_test.messages), 0)
        self.assertEqual(len(good_test.followers), 0)

        # Same email fail register
        with self.assertRaises(IntegrityError):
            db.session.add(User.signup(
                "bad_test", "good_test@email.com", "password", None))
            db.session.commit()
        db.session.rollback()

        # Same username fail register
        with self.assertRaises(IntegrityError):
            db.session.add(User.signup(
                "good_test", "bad_test@email.com", "password", None))
            db.session.commit()
