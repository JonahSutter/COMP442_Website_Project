# flask server imports
from flask import Flask, render_template, request, redirect, url_for, abort 
from flask import session, flash
import os
# security imports
import base64 
from cryptography.fernet import Fernet
from passlib.hash import argon2
# database imports
import sqlite3
from flask import g

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# generate a random secret key
app.config["SECRET_KEY"] = os.urandom(32)

# PASSWORD AND SECURITY

# generate key and pepper
# add: store in secure location
key = Fernet.generate_key()
pep = Fernet(key)

# hash the given password using the pepper
# returns the hashed password
def hash_password(pwd, pep):
    h = argon2.using(rounds=10).hash(pwd)
    ph = pep.encrypt(h.encode('utf-8'))
    b64ph = base64.b64encode(ph)
    return b64ph

# check if given password matches the encrypted b64ph password
# returns true if match, else returns false
def check_password(pwd, b64ph, pep):
    ph = base64.b64decode(b64ph)
    h = pep.decrypt(ph)
    return argon2.verify(pwd, h)

# DATABASE
# get relative path to database file
scriptdir = os.path.dirname(__file__)
DATABASE = os.path.join(scriptdir, "database/chess_data.sqlite3")

# returns a connection to the database
# if the database is not created, creates the table
# add: change create table code
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        c = db.cursor()
        c.execute('''
            create Table Users(
            id int AUTO_INCREMENT primary key,
            email text,
            hash text
            );
        ''')
        db.commit()
    return db

# called when page closed, closes connection to database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ACTIVE LOGIN

# ROUTES

# default route of server, routes client to login page
# add: create database if not created
@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("get_login"))

# post handler for login
# first checks if login button pressed, then validates email and password
# if valid routes to main_page.html, else refreshes page
# add: hash password and see if its in the database, add user info to login session
# add: add a way to login as an administrator
@app.route("/login/", methods=["POST"])
def login():
    if request.form.get("login-button"):
        data = dict()
        fields = ["login-name", "login-password"]
        for field in fields:
            data[field] = request.form.get(field)
        valid = True
        for field in fields:
            if data[field] is None or data[field] == "":
                valid = False
                flash(f"{field} cannot be blank")
        if valid and len(data["login-password"]) < 8:
            valid = False
            flash("password must be at least 8 characters")
        if valid:
            return redirect(url_for("main"))
        else:
            return redirect(url_for("login"))
    flash("Invalid Login")
    return redirect(url_for("login"))

# post handler for login, displays login.html
@app.route("/login/", methods=["GET"])
def get_login():
    return render_template("login.html")

# post handler for main
# add: search function for user
# add: waiting for requirements
@app.route("/main/", methods=["POST"])
def main():
    return render_template("main_page.html")

# get handler for main, displays main_page.html
# add: only display if user info is in login session, else route to login
@app.route("/main/", methods=["GET"])
def get_main():
    return render_template("main_page.html")

# post handler for game
# add: waiting for requirements
@app.route("/game/", methods=["POST"])
def game():
    return render_template("game_page.html")

# get handler for game, displays game_page.html
# add: only display if user info in login session, else route to login
# add: waiting for requirements
@app.route("/game/", methods=["GET"])
def get_game():
    return render_template("game_page.html")

# post handler for edit
# add: validation for changes 
@app.route("/edit/", methods=["POST"])
def edit():
    return render_template("edit_account.html")

# get handler for edit, displays edit_account.html
# add: only display if user info in login session, else route to login
@app.route("/edit/", methods=["GET"])
def get_edit():
    return render_template("edit_account.html")

# post handler for create
# validates username and password, if valid redirects to login
# add: add new information to database
@app.route("/create/", methods=["POST"])
def create():
    data = dict()
    fields = ["create-name", "create-password", "create-confirm-password"]
    for field in fields:
        data[field] = request.form.get(field)
    valid = True
    for field in fields:
        if data[field] is None or data[field] == "":
            valid = False
            flash(f"{field} cannot be blank")
    if valid and len(data["create-password"]) < 8:
        valid = False
        flash("password must be at least 8 characters")
    if valid and data["create-password"] != data["create-confirm-password"]:
        valid = False
        flash("password and confirm password must match")
    if valid:
        # route to login and make user sign in
        return redirect(url_for("login"))
    else:
        # if invalid, route back to creation
        flash("Invalid Account Creation")
        return redirect(url_for("create"))

# get handler for create, displays create_account.html
# add: only display if user info in login session, else route to login
@app.route("/create/", methods=["GET"])
def get_create():
    return render_template("create_account.html")