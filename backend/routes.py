import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from backend import app, db
from backend.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm)
from backend.models import User
from flask_login import login_user, logout_user, current_user, login_required
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = list(db.posts.find().sort('date_posted', -1).skip((page - 1) * 5).limit(5))
    return render_template('home.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = {
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password,
            "image_file": "default.jpg"
        }
        db.users.insert_one(user)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({"email": form.email.data})
        if user and check_password_hash(user['password'], form.password.data):
            login_user(User(user), remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login was successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": {"image_file": picture_file}})
        db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": {"username": form.username.data, "email": form.email.data}})
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = {
            "title": form.title.data,
            "content": form.content.data,
            "author": current_user.id,
            "date_posted": datetime.utcnow()
        }
        db.posts.insert_one(post)
        flash('Your post has been created', 'success')
        return jsonify({'message': 'Post created successfully!'}), 201
    return jsonify({'error': 'Invalid data'}), 400

@app.route("/post/<post_id>")
def post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post:
        return render_template('post.html', title=post['title'], post=post)
    else:
        abort(404)

@app.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post['author'] != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {"title": form.title.data, "content": form.content.data}})
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post['title']
        form.content.data = post['content']
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post['author'] != current_user.id:
        abort(403)
    db.posts.delete_one({"_id": ObjectId(post_id)})
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = db.users.find_one({"username": username})
    if not user:
        abort(404)
    posts = list(db.posts.find({"author": user['_id']}).sort('date_posted', -1).skip((page - 1) * 5).limit(5))
    return render_template('user_posts.html', posts=posts, user=user)
