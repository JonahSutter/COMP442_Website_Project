from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/login/")
def login():
    return render_template("login.html")