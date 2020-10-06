from librarymanagement import app
from flask import render_template

@app.route("/",methods=["GET","POST"])
def login():
    return render_template("login.html")
