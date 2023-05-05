"""Message View tests."""
from models import Message, User
from unittest import TestCase
from app import app, CURR_USER_KEY, db
import os
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


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
        db.session.flush()

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_login_get_request(self):
        """Successful get request for login page"""
        with self.client as c:
            resp = c.get("/login")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<!-- Login page -->", html)

    def test_valid_login(self):  # FIXME:
        """ successful post request test"""
        with self.client as c:
            resp = c.post("/login",
                          data={
                              "username": "u1",
                              "password": "password",
                          },
                          follow_redirects=True
                          )

            html = resp.get_data(as_text=True)

            self.assertIn("u1", html)
            self.assertIn("Homepage for logged in", html)

    def test_invalid_login(self):  # FIXME:
        """ Failed post request test"""
        with self.client as c:
            resp = c.post("/login",
                          data={
                              "username": "u1",
                              "password": "Wrong_Password",
                          },
                          follow_redirects=True

                          )

            html = resp.get_data(as_text=True)

            self.assertIn("<!-- Login page -->", html)
            self.assertIn("Invalid credentials", html)

    def test_signup_get(self):
        """ Get request for signup page"""

        with self.client as c:
            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<!-- NewUser Signup Page -->", html)

    def test_signup_post(self):  # FIXME:
        """Post Request to register new user"""

        with self.client as c:
            resp = c.post("/login",
                          data={
                              "username": "u3",
                              "password": "tatersalad",
                              "email": "email@email.gov",
                              "image_url": "",
                          },
                          follow_redirects=True
                          )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<!-- Homepage for logged in -->", html)

    def test_list_users(self):
        """Test list_users page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("u1", html)
            self.assertIn("u2", html)
            self.assertIn("<!-- User/Index html page -->", html)

    def test_show_user(self):
        """Test to render users details page """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("u1", html)
            self.assertIn("<!-- User's Profile Page -->", html)


# with self.client as c:
#     with c.session_transaction() as sess:
#         sess[CURR_USER_KEY] = self.u1_id
#     resp = c.post(
#         f"/messages/{self.m1_id}/delete", follow_redirects=True)
#     html = resp.get_data(as_text=True)
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
