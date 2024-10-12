from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "http://localhost:3000"}})

app.config["MONGO_URI"] = "mongodb://localhost:27017/ToDoApp"  # Lokale MongoDB oder MongoDB Atlas URI

mongo = PyMongo(app)

# Beispiel-Collection
db = mongo.db


from backend import routes