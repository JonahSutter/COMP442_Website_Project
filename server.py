from flask import Flask, render_template, request, redirect, url_for, abort 
from flask import session, flash
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# generate a random secret key
app.config["SECRET_KEY"] = os.urandom(32)

# default route of server, routes client to login page
@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("get_login"))

# get and post routes to login.html
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

@app.route("/login/", methods=["GET"])
def get_login():
    return render_template("login.html")

# get and post routes to main_page.html
@app.route("/main/", methods=["POST"])
def main():
    return render_template("main_page.html")

@app.route("/main/", methods=["GET"])
def get_main():
    return render_template("main_page.html")

# get and post routes to game_page.html
@app.route("/game/", methods=["POST"])
def game():
    return render_template("game_page.html")

@app.route("/game/", methods=["GET"])
def get_game():
    return render_template("game_page.html")

# get and post routes to edit_account.html
@app.route("/edit/", methods=["POST"])
def edit():
    return render_template("edit_account.html")

@app.route("/edit/", methods=["GET"])
def get_edit():
    return render_template("edit_account.html")

# get and post routes to create_account.html
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

@app.route("/create/", methods=["GET"])
def get_create():
    return render_template("create_account.html")