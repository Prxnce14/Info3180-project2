# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField , BooleanField
from wtforms.validators import InputRequired, Email, DataRequired

#This is the name that will bbe displayed above your input fields


#forms for Posts

class PostForm(FlaskForm):
    photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'],'Image only!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])    



#forms for Likes



#forms for Follows


#Forms for users

class UsersForm(FlaskForm):
    uname = StringField('username ', validators=[InputRequired()])
    password = StringField('Password ', validators=[InputRequired()])
    firstname = StringField('First Name ', validators=[InputRequired()])
    lastname = StringField('Last Name ', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location ', validators=[InputRequired()])
    biography = TextAreaField('Biography ', validators=[InputRequired()])
    photofile = FileField('Photo', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG, JPG, and PNG images are allowed!')
    ])


#Login form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    



