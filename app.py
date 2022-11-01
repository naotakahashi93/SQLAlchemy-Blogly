"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def home():
    all_users = Users.query.all()
    return render_template ("home.html", all_users = all_users)


@app.route("/userform")
def add_user():
     return render_template ("userform.html") 

@app.route("/userinfo",  methods = ["POST"])
def userinfo():
    first = request.form['first']
    last = request.form['last']
    image = request.form['image']

    user = Users(first_name = first, last_name = last, image_url = image)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")
 
@app.route("/<int:user_id>")
def show_userinfo(user_id):
    user = Users.query.get(user_id)
    return render_template ("/showuserinfo.html", user = user)


@app.route("/<int:user_id>/delete", methods = ["POST"])
def delete(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ("/")

@app.route("/<int:user_id>/edit")
def edit(user_id):
    user = Users.query.get(user_id)
    return render_template("editform.html", user=user)

@app.route("/<int:user_id>/edit", methods = ["POST"])
def save_edits(user_id):

    user = Users.query.get(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()
    return redirect ("/")
