from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "storage/data.json"

if not os.path.exists("storage"):
    os.makedirs("storage")
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message.html", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")

        if username and message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

            new_data = {timestamp: {"username": username, "message": message}}
            new_data.update(data) 

            with open(DATA_FILE, "w") as f:
                json.dump(new_data, f, indent=4)

            return redirect(url_for("message"))

    return render_template("message.html")

@app.route("/read")
def read():
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    return render_template("read.html", messages=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

