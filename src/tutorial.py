'''from flask import Flask, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "templates/app.html"

@app.route("/<name>")
def user(name):
    return f"Hello {name}"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="admin!"))

if __name__ == "__main__":
    app.run()'''