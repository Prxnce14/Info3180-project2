# Add any model classes for Flask-SQLAlchemy here

# model for Posts
from . import db
import pytz
from datetime import datetime
from werkzeug.security import generate_password_hash

class Posts(db.Model):

    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('Likes', backref='post', lazy=True)
    created_on = db.Column(db.DateTime())


    def __init__(self, caption, photo, uid):
        self.caption = caption
        self.photo = photo
        self.user_id = uid
        self.created_on =  datetime.now(pytz.timezone('US/Eastern'))

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 suppor
        
    def __repr__(self):
        return '<post: %r>' % self.id



#model for likes

class Likes(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
   

    def __init__(self, post_id, user_id):
        self.user_id = user_id
        self.post_id = post_id


    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<like: %r>' % self.id


# #model for Follows

class Follows(db.Model):

    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, foll_id ,user_id):
        self.followed_user_id = foll_id
        self.user_id = user_id


    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<follows: %r>' % (self.id)


# #model for Users

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())
    posts = db.relationship('Posts', backref='user', lazy=True)
    likes = db.relationship('Likes', backref='user', lazy=True)
    follows = db.relationship('Follows', backref='follower', lazy=True, foreign_keys='Follows.user_id')
    followed_by = db.relationship('Follows', backref='followed_user', lazy=True, foreign_keys='Follows.followed_user_id')


    def __init__(self, uname, pword, fname, lname, em, local, bio, pphoto):
        self.username = uname
        self.password = generate_password_hash(pword, method='pbkdf2:sha256')
        self.firstname = fname
        self.lastname = lname
        self.email = em
        self.location = local
        self.biography = bio
        self.profile_photo = pphoto
        self.created_on = datetime.now(pytz.timezone('US/Eastern'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def get_username(self):
        return self.username
        
    def __repr__(self):
        return '<User %r>' % self.username