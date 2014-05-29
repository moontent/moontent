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

@app.route("/<userid>/posts")
def get_posts(userid):
    def post_to_dict(post):
        return dict(id=post.id, user_id=post.user_id, content=post.content, created_at=post.created_at.isoformat())

    posts = model.all_posts_for_user(userid)
    posts_dicts = [post_to_dict(post) for post in posts]
    return json.dumps(posts_dicts)

if __name__ == "__main__":
    app.run(debug = True)