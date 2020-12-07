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
import datetime
from datetime import timedelta, datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# generate a random secret key
app.config["SECRET_KEY"] = "hotdogmuffinmordorelrondbugsniper"

# Path to website directory
serverdir = os.path.dirname(__file__)

# PASSWORD AND SECURITY

# get relative path to pepper file
pepfile = os.path.join(serverdir, "pepper.bin")
# generate key and pepper
with open(pepfile, 'rb') as fin:
    key = fin.read()
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
DATABASE = os.path.join(serverdir, "chess_data.sqlite3")

# returns a connection to the database
# if the database is not created, creates the table
# add: change create table code
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        c = db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT(100) NOT NULL,
            password BLOB NOT NULL,
            profileimg TEXT(255),
            chessboard TEXT(1000),
            score INTEGER NOT NULL,
            isadmin INTEGER NOT NULL
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

def check_login():
    uid = session.get("uid")
    try:
        exp = datetime.strptime(session.get("expires"), "Y-%m-%dT%H:%M:%SZ")
    except TypeError:
        exp = None
        return redirect(url_for("get_login"))
    except ValueError:
        exp = None
        return redirect(url_for("get_login"))
    conn = get_db()
    c = conn.cursor()
    user = c.execute('select * from Users where id=?;',(uid,))
    conn.commit()
    if user is None or exp is None or exp < datetime.utcnow():
        #print('Valid user')
        #print(user)
        #print(exp)
        return redirect(url_for("get_login"))

# ROUTES

# default route of server, routes client to login page
# add: create database if not created
@app.route("/", methods=["GET"])
def index():
    session.pop("uid", None)
    return redirect(url_for("get_login"))

# post handler for login
# validates username and password
# if valid routes to main_page.html, else refreshes page
# TODO: add a way to login as an administrator
# TODO: add user to login session (user authentication slides)
@app.route("/login/", methods=["POST"])
def login():
    data = dict()
    fields = ["login-name", "login-password"]
    for field in fields:
        data[field] = request.form.get(field)
    user_name = data["login-name"]
    pwd = data["login-password"]
    valid = True
    for field in fields:
        if data[field] is None or data[field] == "":
            valid = False
            flash(f"{field} cannot be blank")
    if valid:
        conn = get_db()
        c = conn.cursor()
        user = c.execute('SELECT id, username, password, score, isadmin FROM Users WHERE username=?;',(user_name,)).fetchone()
        conn.commit()
        if user is not None and check_password(pwd, user[2], pep):
            expires = datetime.utcnow()+timedelta(hours=24)
            session["uid"] = user[0]
            session["expires"] = expires.strftime("Y-%m-%dT%H:%M:%SZ")
            session["username"] = user[1]
            session["score"] = user[3]
            isadmin = user[4]
            if isadmin == 1:
                return redirect(url_for("get_admin"))    
            return redirect(url_for("main"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))
    return "Invalid email or password", 401


# post handler for login, displays login.html
@app.route("/login/", methods=["GET"])
def get_login():
    session.pop("uid", None)
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
    check_login()
    uid = session.get("uid")
    conn = get_db()
    c = conn.cursor()
    user = c.execute('SELECT id, profileimg from Users where id=?',(uid,)).fetchone()
    top_users = c.execute('select username, score, profileimg from Users order by score desc limit 3;').fetchall()
    conn.commit()
    if user is not None and top_users is not None:
        username = session.get("username")
        score = session.get("score")
        profileimg = user[1]
        return render_template("main_page.html", username=username, score=score, top_users=top_users, profileimg=profileimg)
    return redirect(url_for("login"))

# post handler for game
# add: waiting for requirements
@app.route("/game/", methods=["POST"])
def game():
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for('get_game'))
    else:
        conn = get_db()
        c = conn.cursor()
        score = c.execute('select score from Users where id=?;',(uid,))
        submission = request.get_json()
        print(submission)
        if submission is not None:
            if (submission.get("status") == "win"):
                score += 100
                c.execute('update Users set score=? where id=?;',(score,uid))
            elif (submission.get("status") == "lose"):
                score -= 50
                c.execute('update Users set score=? where id=?;',(score,uid))
            elif (submission.get("status") == "draw"):
                score += 10
                c.execute('update Users set score=? where id=?;',(score,uid))
        else:
            print("Could not determine state of game")
        conn.commit()    
        # Send them back to the home page
        return redirect(url_for('get_main'))
    return render_template("game_page.html")

# get handler for game, displays game_page.html
# add: only display if user info in login session, else route to login
# add: waiting for requirements
@app.route("/game/", methods=["GET"])
def get_game():
    check_login()
    uid = session.get("uid")
    conn = get_db()
    c = conn.cursor()
    user = c.execute('SELECT id from Users where id=?',(uid,))
    conn.commit()
    if user is not None:
        return render_template("game_page.html")
    return redirect(url_for("login"))

# post handler for edit
# add: validation for changes 
@app.route("/edit/", methods=["POST"])
def edit():
    name = request.form.get("name")
    pwd = request.form.get("password")
    raw_img = request.form.get("picture-holder")
    img = raw_img.replace('http://localhost:5000','')
    print(img)
    valid = True
    if name is None and name == "":
        flash("Username cannot be blank")
        valid = False
    if valid and pwd is not None and pwd != "":
        if len(pwd) < 8:
            flash("Password must be longer than 8 characters")
            valid = False
    if valid and img is None and img == "":
        flash("Profile image cannot be blank")
        valid = False
    if valid:
        uid = session.get("uid")
        conn = get_db()
        c = conn.cursor()
        if pwd is not None and pwd != "":
            hpwd = hash_password(pwd, pep)
            c.execute('update Users set username=?, password=?, profileimg=? where id=?;',(name,hpwd,img,uid))
        else:
            c.execute('update Users set username=?, profileimg=? where id=?;',(name,img,uid))
        conn.commit()
    return redirect(url_for('get_edit'))

# get handler for edit, displays edit_account.html
# add: only display if user info in login session, else route to login
@app.route("/edit/", methods=["GET"])
def get_edit():
    check_login()
    uid = session.get("uid")
    conn = get_db()
    c = conn.cursor()
    user = c.execute('SELECT username, score, profileimg from Users where id=?;',(uid,)).fetchone()
    conn.commit()
    if user is not None:
        username = user[0]
        score = user[1]
        profileimg = user[2]
        return render_template("edit_account.html", username=username, score=score, profileimg=profileimg)
    return redirect(url_for("login"))

# post handler for create
# validates username and password, if valid redirects to login
# add: add new information to database
@app.route("/create/", methods=["POST"])
def create():
    data = dict()
    fields = ["create-name", "create-password", "create-confirm-password"]
    for field in fields:
        data[field] = request.form.get(field)
    user_name = data["create-name"]
    password = data["create-password"]
    valid = True
    for field in fields:
        if data[field] is None or data[field] == "":
            valid = False
            flash(f"{field} cannot be blank")
    if valid and len(password) < 8:
        valid = False
        flash("password must be at least 8 characters")
    if valid and password != data["create-confirm-password"]:
        valid = False
        flash("password and confirm password must match")
    if valid:
        conn = get_db()
        c = conn.cursor()
        uid = c.execute('SELECT id FROM Users WHERE username=?;',(user_name,)).fetchone()
        if uid is not None:
            flash("An account with this username already exists")
            return redirect(url_for("get_create"))
        hpwd = hash_password(password, pep)
        # NOTE: to create admin account change value for admin to be a 1
        isadmin = 0
        score = 0
        c.execute('INSERT INTO Users (username, password, score, isadmin) VALUES (?,?,?,?);',(user_name, hpwd, score, isadmin))
        conn.commit()
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
    check_login()
    return render_template("create_account.html")

# GET handler to display search results
@app.route("/search/", methods=["POST"])
def get_results():
    check_login()
    search = request.form.get("search")
    if search is None:
        return redirect(url_for('get_main'))
    conn = get_db()
    c = conn.cursor()
    results = c.execute('select username, score, profileimg from Users where username like ?;',('%'+search+'%',))
    conn.commit()
    return render_template("display_users.html", results=results)

@app.route("/submitgame/", methods=["POST"])
def submit_game():
    print("Game submitted")
    submission = request.get_json()
    for key in submission:
        print(key + ": " + str(submission[key]))
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for('get_game'))
    else:
        conn = get_db()
        c = conn.cursor()
        score = c.execute('select score from Users where id=?;',(uid,))
        print(submission)
        if submission is not None:
            if (submission.get("status") == "win"):
                score += 100
                c.execute('update Users set score=? where id=?;',(score,uid))
            elif (submission.get("status") == "lose"):
                score -= 50
                c.execute('update Users set score=? where id=?;',(score,uid))
            elif (submission.get("status") == "draw"):
                score += 10
                c.execute('update Users set score=? where id=?;',(score,uid))
        else:
            print("Could not determine state of game")
        conn.commit()    
        # Send them back to the home page
        return redirect(url_for('get_main'))

@app.route("/admin/", methods=["GET"])
def get_admin():
    check_login()
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for('get_login'))
    conn = get_db()
    c = conn.cursor()
    all_users = c.execute('select username, profileimg, score, id from Users').fetchall()
    conn.commit()
    return render_template("admin.html", all_users=all_users)

@app.route("/admin/", methods=["POST"])
def post_admin():
    delete_user = request.form.get("delete")
    if delete_user is not None:
        conn = get_db()
        c = conn.cursor()
        c.execute('delete from Users where id=?;',(delete_user,))
        conn.commit()
    return redirect(url_for('get_admin'))