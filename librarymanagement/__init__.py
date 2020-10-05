from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Flask_LMS.db"
db = SQLAlchemy(app)

from librarymanagement import routes