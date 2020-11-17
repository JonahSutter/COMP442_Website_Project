from flask import Flask, render_template, request, redirect, url_for, abort 
from flask import session, flash
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = os.urandom(32)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect(url_for("login"))
    if request.method == "POST":
        data = dict()
        return redirect(url_for("main_page"))
    else:
        return render_template("login.html")

@app.route("/main/", methods=["GET, POST"])
def main():
    if request.method == "GET":
        return render_template("main_page.html")

@app.route("/game/", methods=["GET, POST"])
def game():
    if request.method == "GET":
        return render_template("game_page.html")

@app.route("/edit/", methods=["GET, POST"])
def edit():
    if request.method == "GET":
        return render_template("edit_account.html")

@app.route("/create/", methods=["GET, POST"])
def create():
    if request.method == "GET":
        return render_template("create_account.html")