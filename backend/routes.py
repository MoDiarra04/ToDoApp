from backend import app, db
from flask import request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime, timezone
from bson.objectid import ObjectId

# Flask-SocketIO initialisieren
socketio = SocketIO(app)

# Speichere alle verbundenen Clients in verschiedenen Räumen
active_rooms = {}

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
        "date_posted": datetime.now(timezone.utc),
    }

    # Überprüfen, ob Titel und Inhalt vorhanden sind
    if not post["title"] or not post["content"]:
        return jsonify({"message": "Title and content are required"}), 400

    try:
        # speichere in der Datenbank
        db.posts.insert_one(post)
        # Echtzeit-Übertragung des neuen Posts an alle Clients
        socketio.emit('new_post', post, broadcast=True)
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
    date_posted = datetime.now(timezone.utc)

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
    #socketio.emit('update_post', updated_post, broadcast=True)

    return jsonify({'message': 'Post updated successfully!'}), 200

    return jsonify({"message": "Post updated successfully!"}), 200  # Good request


@app.route("/post/<post_id>/delete", methods=["DELETE"])
def delete_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    db.posts.delete_one({"_id": ObjectId(post_id)})
    
    # Informiere alle Clients über das Löschen des Posts
    socketio.emit('delete_post', {'post_id': post_id}, broadcast=True)

    return jsonify({"message": "Your post has been deleted!"}), 204

# WebSocket-Ereignisse für gemeinsames Arbeiten
@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)
    active_rooms[room] = active_rooms.get(room, [])
    active_rooms[room].append(request.sid)
    emit('message', {'message': f'User has joined room {room}'}, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)
    if room in active_rooms and request.sid in active_rooms[room]:
        active_rooms[room].remove(request.sid)
    emit('message', {'message': f'User has left room {room}'}, room=room)

@socketio.on('mark_post')
def handle_mark_todo(data):
    post_id = data['post_id']
    status = data['status']
    db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {"completed": status}})
    
    # Benachrichtige alle Clients über den geänderten Status
    emit('todo_marked', {'post_id': post_id, 'status': status}, broadcast=True)

@socketio.on('update_post')
def handle_update_post(data):
    post_id = data.get('post_id')
    updates = {}

    if 'title' in data:
        updates['title'] = data['title']
    if 'content' in data:
        updates['content'] = data['content']

    if updates:
        db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": updates})

    emit('post_updated', {'message': 'Post updated successfully!'})

@socketio.on('delete_post')
def handle_delete_post(data):
    post_id = data['post_id']
    db.posts.delete_one({"_id": ObjectId(post_id)})
    
    # Benachrichtige alle Clients über das gelöschte ToDo
    emit('delete_post', {'post_id': post_id}, broadcast=True)
