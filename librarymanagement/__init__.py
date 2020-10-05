from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///LMS.db"
app.config['SECRET_KEY']="Hello"
db = SQLAlchemy(app)

from librarymanagement import routes