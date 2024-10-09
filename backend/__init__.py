import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"  # Lokale MongoDB oder MongoDB Atlas URI

mongo = PyMongo(app)

# Beispiel-Collection
db = mongo.db


from backend import routes