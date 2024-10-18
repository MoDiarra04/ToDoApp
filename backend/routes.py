from backend import app, db
from flask import request,jsonify
from datetime import datetime, timezone
from bson.objectid import ObjectId
{

}
@app.route("/posts",methods=["GET"])
def get_all_posts():
    posts = []
    for post in db.posts.find():
        posts.append(post)
    return jsonify({"posts": posts})

@app.route("/post/new", methods=['POST'])
def new_post():
    post = {
        "title": request.json.get("title"),
        "content": request.json.get("content"),
        "author": request.json.get("author"),
        "date_posted": datetime.now(timezone.utc)
    }
    # Überprüfen, ob Titel und Inhalt vorhanden sind
    if not post["title"] or not post["content"]:
        return jsonify({"message": "Title and content are required"}), 400  # HTTP-Status 400: Bad Request

    try:
        #speichere in der Datenbank
        db.posts.insert_one(post)
    except Exception as e:
        return jsonify({"message":str(e)}), 400

    return jsonify({'message': 'Post created successfully!'}), 201 # Good request

@app.route("/post/<post_id>/update", methods=['PATCH'])
def update_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"message":"Post not found"})
    data = request.json
    title = data.get("title",post["title"])
    content = data.get("content",post["content"])
    author = data.get("author",post["author"])
    date_posted = data.get("date_posted","date_posted")
    db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {"title": title, "content": content, "author":author, "date_posted": date_posted}})
    return jsonify({'message': 'Post updated successfully!'}), 200 # Good request

@app.route("/post/<post_id>/delete", methods=['DELETE'])
def delete_post(post_id):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    # Überprüfen, ob der Post existiert
    if post is None:
        return jsonify({"error": "Post not found"}), 404  # HTTP-Status 404: Not Found

    db.posts.delete_one({"_id": ObjectId(post_id)})
    
    return jsonify({"message": "Your post has been deleted!"}), 204  # HTTP-Status 204: No Content