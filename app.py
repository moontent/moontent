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

if __name__ == "__main__":
    app.run(debug = True)