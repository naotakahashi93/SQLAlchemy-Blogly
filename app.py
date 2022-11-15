"""Blogly application."""

from site import addusersitepackages
from flask import Flask, request, redirect, render_template
from models import PostTag, db, connect_db, Users, Post, Tag

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
    all_posts = Post.query.all()
    return render_template ("/showuserinfo.html", user = user, all_posts = all_posts)


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

@app.route("/<int:user_id>/posts/new")
def create_post(user_id):
    """Show form to add a post for that user."""
    user = Users.query.get(user_id)
    all_tags = Tag.query.all()
    return render_template("postform.html", user = user, all_tags = all_tags)


@app.route("/<int:user_id>/posts/new", methods= ["POST"])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = Users.query.get(user_id)
    new_post = Post(title = request.form['post-title'], 
                    content = request.form['post-content'],
                    user_id = user.id
    )
    db.session.add(new_post)
    db.session.commit()
    selectedtags = request.form.getlist("tags") ## getting the list of all tags that was selected for this post

    for tag in selectedtags: ## looping over each tag 
        addtag = Tag.query.get(tag) ## getting that tag (each tag is the tag.id)
        new_post.tags.append(addtag) ## adding that to this post instance
    
    db.session.commit()
    return redirect(f"/{user.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post and buttons to edit and delete the post."""
    post = Post.query.get(post_id)
    return render_template("showpost.html", post = post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get(post_id)
    all_tags = Tag.query.all()
    return render_template("editpost.html", post = post, all_tags =all_tags)


@app.route("/posts/<int:post_id>/edit", methods= ["POST"])
def save_post_edits(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get(post_id)
    post.title = request.form['post-title']
    post.content = request.form['post-content']
    selectedtags = request.form.getlist("tags") ## getting the list of all tags that was selected for this post
    post.tags = Tag.query.filter(Tag.id.in_(selectedtags)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods= ["POST"])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect (f"/{post.user_id}")

@app.route("/tags")
def tagslist():
    """Lists all tags, with links to the tag detail page."""
    all_tags = Tag.query.all()
    return render_template("tagslist.html", all_tags = all_tags)

@app.route("/tags/<int:tag_id>")
def tagsinfo(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get(tag_id)
    all_post = Post.query.all()
    return render_template("tagsinfo.html", tag=tag, all_post = all_post)

@app.route("/tags/new")
def newtagform():
    """Shows a form to add a new tag."""
    return render_template("newtagform.html")

@app.route("/tags/new", methods =["POST"])
def addtag():
    """Process add form, adds tag, and redirect to tag list."""
    tagname = request.form["tag-name"]
    newtag = Tag(name=tagname)
    db.session.add(newtag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<tag_id>/edit")
def editform(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get(tag_id)
    return render_template("tageditform.html", tag=tag)

@app.route("/tags/<tag_id>/edit", methods=["POST"])
def processedit(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    tag = Tag.query.get(tag_id)
    tag.name = request.form["tag-name"]
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<tag_id>/delete", methods=["POST"])
def deletetag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")