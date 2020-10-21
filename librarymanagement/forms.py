from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length,Email

class loginForm(FlaskForm):
    #email format looks odd. Why username is present? Let's go with email as necessity for logging in?
    #maybe use: email = StringField('Email', validators=[DataRequired(), Email()])?

    email=StringField('Email',validators=[DataRequired(message="username can't be empty"),Length(min=5,message="username has to be greater than 5")])
    password=PasswordField('Password',validators=[DataRequired(message="Password can't be empty")])
    login=SubmitField('Login')

class issueForm(FlaskForm):
    memberId = IntegerField('MemberId', validators = [DataRequired(message = "Member id can't be empty")])
    #Check for the following line. If it doesn't work, try dropping the () of today
    date = DateTimeField('Date', default = date.today())
    #Check the following. Make the ints to strings in choices if any problem.
    bookId = IntegerField('BookId')
    #Check the following code. 'Add' instead of 'issue'?
    issueDetails = SubmitField('issue')

class returnForm(FlaskForm):
    memberId2 = IntegerField('MemberId2', validators = [DataRequired(message = "Member id can't be empty")])
    returnDetails = SubmitField('return')

    