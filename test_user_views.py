"""Message View tests."""
import os

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


from app import app, CURR_USER_KEY, db

from unittest import TestCase

from models import Message, User

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
FLASK_DEBUG = False

# This is a bit of hack, but don't use Flask DebugToolbar

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserModelCredentialsTestCase(TestCase):
    """Test of User class and Follow class/ join table"""

    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

        with self.client as c:
            resp = c.post("/login",
                          data={
                              "username": "u1",
                              "password": "password",
                          },
                          )

    def tearDown(self):
        db.session.rollback()


"""Does is_following successfully detect when user1 is following user2?
Does is_following successfully detect when user1 is not following user2?
Does is_followed_by successfully detect when user1 is followed by user2?
Does is_followed_by successfully detect when user1 is not followed by user2?
Does User.signup successfully create a new user given valid credentials?
Does User.signup fail to create a new user if any of the validations (eg uniqueness, non-nullable fields) fail?
Does User.authenticate successfully return a user when given a valid username and password?
Does User.authenticate fail to return a user when the username is invalid?
Does User.authenticate fail to return a user when the password is invalid?
Does anon-user have access to user detail pages
"""
