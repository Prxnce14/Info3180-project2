# Add any model classes for Flask-SQLAlchemy here

# model for Posts
from . import db

class Posts(db.Model):

    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime())


    def __init__(self, caption, photo, uid, create ):
        self.caption = caption
        self.photo = photo
        self.user_id = uid
        self.created_on = create
        
    def __repr__(self):
        return '<insiders %r>' % self.title



#model for likes

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    
    def __init__(self,post_id,user_id):
        self.user_id = user_id
        self.post_id = post_id


#model for Follows

class Follows(db.Model):

    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    
    def __init__(self,foll_id,user_id):
        self.follower_id = foll_id
        self.user_id = user_id



#model for Users

class Users(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())


    def __init__(self, uname, pword, fname, lname, em, local, bio, pphoto, create):
        self.username = uname
        self.password = pword
        self.firstname = fname
        self.lastname = lname
        self.email = em
        self.location = local
        self.biography = bio
        self.profile_photo = pphoto
        self.created_on = create
        
    def __repr__(self):
        return '<insiders2 %r>' % self.title