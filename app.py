"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "zipit"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()



# User Routes:

@app.route('/')
def go_to_users():
    """Redirects to users route."""

    return redirect('/users')


@app.route('/users')
def show_users():
    """Shows list of all users."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_add_form():
    """Shows form to add a new user."""

    return render_template('add-form.html')


@app.route('/users/new', methods=["POST"])
def handle_add_form():
    """Takes info from the add form, and adds it to the users table."""

    first_name = request.form["first"]
    last_name = request.form["last"]
    image_url = request.form["image"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Shows details of a particular user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).order_by(Post.title).all()

    return render_template('details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Shows form to edit a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_form(user_id):
    """Takes info from edit form and updates the user in the table."""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.image_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user from the table."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')



# Post Routes:

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows form to create a new post, from a specific user."""

    user = User.query.get_or_404(user_id)
    return render_template('post-form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post_form(user_id):
    """Takes info from the add post form and updates the 'posts' table."""

    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        user_id = user_id
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows specific post details."""

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Shows form to edit a particular post."""

    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post_form(post_id):
    """Takes edited info from the edit form and updates the 'posts' table accordingly."""

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Saves the user_id, then deletes the post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    post.delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')