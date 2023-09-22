"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "zipit"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def go_to_users():
    """Redirects to users route"""

    return redirect('/users')


@app.route('/users')
def show_users():
    """Shows list of all users"""

    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_add_form():
    """Shows form to add a new user"""

    return render_template('add-form.html')


@app.route('/users/new', methods=["POST"])
def handle_add_form():
    """Takes info from the add form, and adds it to the users table"""

    first_name = request.form["first"]
    last_name = request.form["last"]
    image_url = request.form["image"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Shows details of a particular user"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Shows form to edit a user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_form(user_id):
    """Takes info from edit form and updates the user in the table"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    user.image_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user form the table"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

