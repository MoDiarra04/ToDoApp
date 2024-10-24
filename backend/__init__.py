from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Init Flask App
app = Flask(__name__)

# Cors regelt Interaktion Frontend und Backend, die auf unterschiedlichen Servern laufen.
# Verhindert, dass Webanwendungen auf Ressourcen von einer anderen Domain zugreifen.
CORS(app,resources={r"/*": {"origins": "http://localhost:3000"}})

# Init database
app.config["MONGO_URI"] = 'mongodb+srv://modiarra04:Slimgym123%2B@cluster0.sacuw.mongodb.net/ToDoApp?retryWrites=true&w=majority'
db = PyMongo(app).db

from backend import routes