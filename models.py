"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    with app.app_context():
        db.init_app(app)
 

class Users(db.Model):
    """Users"""

    __tablename__  = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                            nullable=False)
    last_name = db.Column(db.Text,
                            nullable=False)
    image_url = db.Column(db.Text,
                            nullable=True,
                            default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

    # def greet(self):
    #     """Greet using first name."""

    #     return f"Hello {self.first_name}"

