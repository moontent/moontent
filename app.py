from flask import Flask, render_template, flash, request, redirect, url_for, session
import model
import json

app = Flask(__name__)
app.secret_key = "howdoievensecretkey"

@app.route("/")
def index():
    return "THIS IS MY APP"

@app.route("/<userid>")
def get_user(userid):
    user = model.get_user(userid)
    user_dict = dict(id=user.id, username=user.username)
    return json.dumps(user_dict)

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    new_user = model.create_user(username, first_name, last_name)

    return str(new_user.id)

@app.route("/<userid>/posts")
def get_posts(userid):
    posts = model.all_posts_for_user(userid)
    return render_posts(posts)

#TODO: move this to like a view i guess?
def render_posts(posts):
    def post_to_dict(post):
        return dict(id=post.id, user_id=post.user_id, content=post.content, created_at=post.created_at.isoformat())

    posts_dicts = [post_to_dict(post) for post in posts]
    return json.dumps(posts_dicts)

@app.route("/<userid>/posts", methods=["POST"])
def create_post(userid):
    content = request.form.get("content")
    post = model.create_post(userid, content)
    return str(post.id)

@app.route("/<userid>/feed")
def get_feed(userid):
    user = model.get_user(userid)
    posts = model.get_feed(user)
    return render_posts(posts)
    
if __name__ == "__main__":
    app.run(debug = True)