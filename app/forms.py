# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

from flask_wtf.file import FileField, FileRequired, FileAllowed

class PostForm(FlaskForm):
    photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'],'Image only!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])    



