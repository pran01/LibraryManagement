from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, DateTimeField, IntegerField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email

class loginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(message="email can't be empty"),Email()])
    password=PasswordField('Password',validators=[DataRequired(message="Password can't be empty")])
    login=SubmitField('Login')

class issueForm(FlaskForm):
    memberId = IntegerField('MemberId', validators = [DataRequired(message = "Member id can't be empty")])
    #Check the following code. 'Add' instead of 'issue'?
    issueDetails = SubmitField('issue')

class returnForm(FlaskForm):
    memberId = IntegerField('MemberId', validators = [DataRequired(message = "Member id can't be empty")])

# class registerForm(FlaskForm):
#     name= StringField('Name',validators=[DataRequired()])
#     email= StringField('Email',validators=[DataRequired(),Email()])
#     isAdult= BooleanField('Adult',validators=[DataRequired()])
#     address=TextAreaField('Address',validators=[DataRequired()])
#     register=SubmitField('Submit')

    