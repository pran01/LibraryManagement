from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import event
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///LMS.db"
app.config['SECRET_KEY']="Hello"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

admin=Admin(app)

from librarymanagement.models import *

@event.listens_for(librarian.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value,method='sha256')
    return value

admin.add_view(ModelView(librarian,db.session))
admin.add_view(ModelView(librarianMobile,db.session))
admin.add_view(ModelView(book,db.session))
admin.add_view(ModelView(bookGenre,db.session))
admin.add_view(ModelView(bookAuthor,db.session))

from librarymanagement import routes