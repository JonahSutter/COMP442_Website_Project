from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/main/")
def main():
    return render_template("main_page.html")

@app.route("/game/")
def game():
    return render_template("game_page.html")

@app.route("/edit/")
def edit():
    return render_template("edit_account.html")

@app.route("/create/")
def create():
    return render_template("create_account.html")