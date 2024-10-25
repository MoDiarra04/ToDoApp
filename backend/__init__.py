from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_socketio import join_room, leave_room, emit, send, SocketIO
from string import ascii_uppercase

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app)

app.config["MONGO_URI"] = 'mongodb+srv://modiarra04:Slimgym123%2B@cluster0.sacuw.mongodb.net/ToDoApp?retryWrites=true&w=majority'

mongo = PyMongo(app)

# Beispiel-Collection
db = mongo.db


from backend import routes