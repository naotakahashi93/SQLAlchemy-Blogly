from unittest import TestCase
from xml.dom import UserDataHandler

from app import app
from models import db, Users

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()


class UsersModelTestCase(TestCase):
    """Tests for model for Uets."""

    def setUp(self):
        """Clean up any existing Users."""

        Users.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_name(self):
        user = Users(first_name="TestFirst", last_name="TestLast", image_url ="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
        self.assertEquals(user.first_name(), "TestFirst")
