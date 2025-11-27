from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes




POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """get all posts and (optional) sort by content or title in ascending or descending order"""
    sort_field = request.args.get("sort")
    sort_direction = request.args.get("direction")

    # 1) no sorting → return original list
    if not sort_field and not sort_direction:
        return jsonify(POSTS), 200

    # 2) validate sort field
    if sort_field not in ("title", "content"):
        return jsonify({"error": "you can only sort by title or content"}), 400

    # 3) validate direction
    if sort_direction not in ("asc", "desc"):
        return jsonify({"error": "you have to enter asc (for ascending) or desc (for descending order"}), 400

    # 4) do the sorting
    reverse = (sort_direction == "desc")
    sorted_list = sorted(POSTS, key=lambda d: d[sort_field].lower(), reverse=reverse)
    return jsonify(sorted_list), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """add new posts"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data was given"}), 400
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"error": "No title or content have been given"}), 400

    unique_id = max(item.get("id") for item in POSTS) +1
    new_post = {"id": unique_id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify({"id": unique_id, "title": title, "content": content}), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """delete posts by id"""
    for item in POSTS:
        if item.get("id") == id:
            POSTS.remove(item)

            return jsonify({"message": f"post with id {id} deleted successfully"}), 200

    return jsonify({"errormessage": "No title found to be deleted"}), 404


@app.route("/api/posts/<int:id>", methods=['PUT'])
def update_posts(id):
    """update posts by id"""
    data = request.get_json()
    for post in POSTS:
        if post.get("id") == id:
            new_title = data.get("title", post.get("title"))
            new_content = data.get("content", post.get("content"))
            post["title"] = new_title
            post["content"] = new_content

            return jsonify({
            "id": id,
            "title": new_title,
            "content": new_content}), 200

    return jsonify({"errormessage": "No post was found for the given ID"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """search for specific characters or words in title or content"""
    # get query parameters
    search_title = request.args.get("title", "").lower()
    search_content = request.args.get("content", "").lower()

    # filter posts
    results = []
    for post in POSTS:
        title_match = search_title in post["title"].lower() if search_title else True
        content_match = search_content in post["content"].lower() if search_content else True

        if title_match and content_match:
            results.append(post)

    return jsonify(results), 200




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
