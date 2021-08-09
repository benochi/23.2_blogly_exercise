"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post #added Post for model update
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhh'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """homepage shows the 5 most recent posts""" #changed from redirect to 5 most recent posts. 
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all() #pulls posts from DB, from all posts, and limits reponse to 5
    return render_template("posts/homepage.html", posts=posts)

@app.route("/users")
def users():
    """Page of all current users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """shows form for new user input"""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def new_users():
    """handles form submission of new_user_form"""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_users():
    """shows a page with info on a user using their user_id"""

    user = User.query.get_or_404(user_id) #if no user found will return the added custom 404 page. 
    return render_template('users/show.html', user=user)

@app.route("/users/<int:user_id>/edit")
def edit_users(user_id):
    """Shows the edit page for a user and a cancel button that returns to the detail page for a user, 
    and a save button that updates the user.""" 

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_users(user_id):
    """Handle the form submission for edit_users"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_users(user_id):
    """Handle the form submission for deleting a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} has been deleted.")

    return redirect("/users")

@app.errorhandler(404) #flask 404 errorhandler route
def error_page(e):
    """custom 404 error page"""
    return render_template('404.html'), 404


#posts routes for Posts model class

@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    """shows form to make a new post for user_id"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_posts_form_submission(user_id):
    """Form submission for new post for user_id"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' has been added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """shows a page that has specific info on a post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """shows a form to edit info on a post"""    
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_posts_form_submission(post_id):
    """post form submission handling"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'] 
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been added.")

    return redirect(f"/users/ {post.user_id}") 

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_posts_form_submission(post_id):
    """Handles form submission to delete a post """

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been deleted.")

    return redirect(f"/users/{post.user_id}")
