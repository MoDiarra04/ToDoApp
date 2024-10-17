from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "http://localhost:3000"}})



app.config["MONGO_URI"] = 'mongodb+srv://modiarra04:Slimgym123%2B@cluster0.sacuw.mongodb.net/ToDoApp?retryWrites=true&w=majority'

mongo = PyMongo(app)

# Beispiel-Collection
db = mongo.db


from backend import routes