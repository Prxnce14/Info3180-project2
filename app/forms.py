# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField 
from wtforms.validators import InputRequired, Email, DataRequired

#This is the name that will bbe displayed above your input fields


#forms for Posts

class PostForm(FlaskForm):
    photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPEG, JPG, and PNG images are allowed!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])    



#Forms for users

class UsersForm(FlaskForm):
    username = StringField('username ', validators=[InputRequired()])
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
    


#Forms for follows

class FollowForm(FlaskForm):
    follower_id = StringField('Target', validators=[InputRequired()])
    user_id = StringField('User', validators=[InputRequired()])