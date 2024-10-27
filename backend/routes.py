from backend import app, db
from flask import request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime
from bson.objectid import ObjectId
from string import ascii_uppercase
import random
from backend import socketio

# Speichert alle verbundenen Clients in verschiedenen Räumen
active_rooms = {}

def generate_unique_code(lenght):
    while True:
        code = ""
        for _ in range(lenght):
            code += random.choice(ascii_uppercase)
        if code not in active_rooms:
            break
    return code

@app.route("/generate_code", methods=['GET'])
def generateRoomCode():
    # Hier Code zum überprüfen ob User schon in einem Room ist
    room = generate_unique_code(4)
    active_rooms[room] = {"members": 0, "posts": [], "members_ID":[]} #user_id
    join_room(room)
    active_rooms[room]["members_ID"].append(request.sid)  # Sitzung-ID hinzufügen
    active_rooms[room]["members"] += 1
    return jsonify(room)

@app.route("/posts", methods=["GET"])
def get_all_posts():

    posts = []
    for post in db.posts.find():
        post['_id'] = str(post['_id'])  # Konvertiere ObjectId in String für JSON
        posts.append(post)
    return jsonify(posts)


@app.route("/post/new", methods=["POST"])
def new_post():
    post = {
        "title": request.json.get("title"),
        "content": request.json.get("content"),
        "author": request.json.get("author"),
        "date_posted": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }

    # Überprüfen, ob Titel und Inhalt vorhanden sind
    if not post["title"] or not post["content"]:
        return jsonify({"message": "Title and content are required"}), 400

    try:
        # speichere in der Datenbank
        db.posts.insert_one(post)

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({'message': 'Post created successfully!'}), 201


@app.route("/post/<post_id>/update", methods=["PATCH"])
def update_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        return jsonify({"message":"Post not found"}), 404

    data = request.json
    title = data.get("title", post["title"])
    content = data.get("content", post["content"])
    author = data.get("author", post["author"])
    date_posted = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    db.posts.update_one({"_id": ObjectId(post_id)}, {
        "$set": {
            "title": title, 
            "content": content, 
            "author": author, 
            "date_posted": date_posted
        }
    })
    
    # Informiere alle Clients über die Aktualisierung des Posts
    updated_post = db.posts.find_one({"_id": ObjectId(post_id)})
    updated_post['_id'] = str(updated_post['_id'])

    return jsonify({'message': 'Post updated successfully!'}), 200

@app.route("/post/<post_id>/delete", methods=["DELETE"])
def delete_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    db.posts.delete_one({"_id": ObjectId(post_id)})

    return jsonify({"message": "Your post has been deleted!"}), 204

# WebSocket-Ereignisse für gemeinsames Arbeiten
@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    active_rooms[room] = active_rooms.get(room, [] )
    # Die ID des aktuellen Clients zu `members_ID` hinzufügen
    active_rooms[room]["members_ID"].append(request.sid) #data[user_id] anstatt request.sid
    # Member-Anzahl erhöhen
    active_rooms[room]["members"] += 1
    emit('message', {'message': f'User has joined room {room}'}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)
    if room in active_rooms and request.sid in active_rooms[room]:
        active_rooms[room]["members_ID"].remove(request.sid)
        active_rooms[room]["members"] -= 1
    emit('message', {'message': f'User has left room {room}'}, room=room)

@socketio.on('update_post')
def handle_update_post(data):
    room = data['room']
    post_id = data.get('post_id')
    updates = {}

    if 'title' in data:
        updates['title'] = data['title']
    if 'content' in data:
        updates['content'] = data['content']

    if updates:
        db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": updates})

    emit('post_updated', {'message': 'Post updated successfully!'}, room=room)

@socketio.on('delete_post')
def handle_delete_post(data):
    room = data['room']
    post_id = data['post_id']
    db.posts.delete_one({"_id": ObjectId(post_id)})
    
    # Benachrichtige alle Clients über das gelöschte ToDo
    emit('delete_post', {'post_id': post_id}, room=room)

@socketio.on('new_post')
def handle_new_post(data):
    room = data['room']
    post = {
        "title": data.get("title"),
        "content": data.get("content"),
        "author": data.get("author"),
        "date_posted": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    # Überprüfen, ob Titel und Inhalt vorhanden sind
    if not post["title"] or not post["content"]:
        emit('error', {"message": "Title and Content are required"}, room=room)
        return

    try:
        # Speichere in der Datenbank
        db.posts.insert_one(post)

        # Sende den neuen Post an alle verbundenen Clients
        emit('new_post', post, room=room)
    except Exception as e:
        emit('error', {"message": str(e)}, room=room)
