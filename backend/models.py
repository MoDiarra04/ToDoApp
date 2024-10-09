from datetime import datetime
from flask import Flask
from backend import db
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

def load_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user)
    return None

# User model for MongoDB
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.email = user_doc['email']
        self.password = user_doc['password']

    @staticmethod
    def get_user_by_username(username):
        user_doc = db.users.find_one({'username': username})
        if user_doc:
            return User(user_doc)
        return None

    @staticmethod
    def create_user(username, email, password):
        user_id = db.users.insert_one({
            'username': username,
            'email': email,
            'image_file': 'default.jpg',
            'password': password,
        }).inserted_id
        return str(user_id)

# Post model for MongoDB
class Post:
    def __init__(self, post_doc):
        self.id = str(post_doc['_id'])
        self.title = post_doc['title']
        self.date_posted = post_doc['date_posted']
        self.content = post_doc['content']
        self.user_id = str(post_doc['user_id'])

    @staticmethod
    def create_post(title, content, user_id):
        post_id = db.posts.insert_one({
            'title': title,
            'date_posted': datetime.utcnow(),
            'content': content,
            'user_id': ObjectId(user_id),
        }).inserted_id
        return str(post_id)

    @staticmethod
    def get_all_posts():
        posts = []
        for post in db.posts.find():
            posts.append(Post(post))
        return posts

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
