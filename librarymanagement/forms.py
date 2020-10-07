from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class loginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(message="username can't be empty"),Length(min=5,message="username has to be greater than 5")])
    password=PasswordField('Password',validators=[DataRequired(message="Password can't be empty")])
    login=SubmitField('Login')
