from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///LMS.db"
db = SQLAlchemy(app)

from librarymanagement import routes