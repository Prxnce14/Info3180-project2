# Add any model classes for Flask-SQLAlchemy here

# model for Posts
from . import db

class insiders(db.Model):

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



#model for 
