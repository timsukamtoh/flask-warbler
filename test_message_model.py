"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py

from models import db, User, Message, Follow, Like
from unittest import TestCase
from app import app
import os

os.environ["DATABASE_URL"] = "postgresql:///warble_test"


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

FLASK_DEBUG = False
# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

        msg1 = Message(text="test", user_id=self.u1_id)
        db.session.add(msg1)
        db.session.commit()

        self.msg1_id = msg1.id

    def tearDown(self):
        db.session.rollback()

    def test_messages_model(self):
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        # User1 should have 1 message, user2 none.
        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(len(u2.messages), 0)

    def test_datatypes(self):
        """check that message data types are correct"""

        msg = Message.query.get(self.msg1_id)

        self.assertIsInstance(msg.id, int)
        self.assertIsInstance(msg.user_id, int)
        self.assertIsInstance(msg.liked_by_users, list)
        self.assertEqual(len(msg.likes), 0)


# TODO: Test the likes - throw some stank on them messages and see if it sticks
