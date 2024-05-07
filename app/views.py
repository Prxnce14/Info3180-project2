import os
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory, make_response
from werkzeug.utils import secure_filename
from app.models import Posts, Users, Likes, Follows
from app.forms import PostForm, LoginForm, UsersForm, FollowForm
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# @app.route('/')
# def home():
#     """Render website's home page."""
#     return render_template('home.html')


#Endpoint for registering a user 

@app.route('/api/v1/register', methods=['POST'])
def create_user():
    
    if request.method =='POST':
        try:
            userform = UsersForm()
            if userform.validate_on_submit():

                print("ready to process the form")
                uname = userform.username.data
                pword = userform.password.data
                fname = userform.firstname.data
                lname = userform.lastname.data
                email = userform.email.data
                local = userform.location.data
                bio = userform.biography.data
                img = userform.photofile.data
                filename = secure_filename(img.filename)
                print("Saving file to:", os.path.join(app.config['UPLOAD_FOLDER'], filename))


                img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_user = Users(uname, pword, fname, lname, email, local, bio, filename)

                db.session.add(new_user)
                db.session.commit()

                flash(f'{uname} Successfully Registered', 'success')

                return jsonify({
                    "message": "User Successfully added",
                    "firstname": fname,
                    "lastname": lname,
                    "username": uname,
                    "password": pword,
                    "email": email,
                    "location": local,
                    "biography": bio,
                    "profile_photo": filename
                })

            else:
                errors = form_errors(userform)
                return jsonify({'errors': errors})

        except Exception as e:
             # Handle any exceptions here
            return jsonify({'error': str(e)}), 500  # Return JSON response for error
            
        

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
       
        try:
            if form.validate_on_submit():
                # Get the username and password values from the form.
                username = form.username.data
                password = form.password.data
                
                # Using your model, query database for a user based on the username
                # and password submitted. Remember you need to compare the password hash.
                # You will need to import the appropriate function to do so.
                # Then store the result of that query to a `user` variable so it can be
                # passed to the login_user() method below.
        
                user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()

                if user is not None and check_password_hash(user.password, password):
                    
                    # If the user is not blank, meaning if a user was actually found,
                    # then login the user and create the user session.
                    # user should be an instance of your `Users class
                    # Gets user id, load into session
                    # login_user(user)
                    login_user(user)

                    id = user.id
                
                    # Generate JWT token
                    access_token = create_access_token(identity=user.id)

                    # Return JWT token to the client
                    return  jsonify({

                    'message': user.username + ' Successfully logged in' ,
                    'id': user.id ,
                    'access_token': access_token 
                    })
                        
                else:
                    flash('Username or Password is incorrect.', 'danger')

            else:
                    errors = form_errors(form)
                    return jsonify({'errors': errors})

        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)
            return jsonify({'error': str(e)}), 500  # Return JSON response for error
            


#Endpoint  for loging out a user

@app.route('/api/v1/auth/logout', methods = ['POST'])
@jwt_required()  # This decorator requires JWT authentication
def logout():
    if request.method == 'POST':
        try:
            logout_user()
            
            # flash('You have been logged out.', 'success')
            
            return jsonify({
                "message": "User successfully logged out."
            })
        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)



#Endpoint for getting user details
from flask import jsonify

@app.route('/api/v1/users/<user_id>', methods=['GET'])
#@jwt_required()  # This decorator requires JWT authentication
#@login_required
def getUserDetails(user_id):
    if request.method == 'GET':
        try:
            user = db.session.execute(db.select(Users).filter_by(id=int(user_id))).scalar()
            posts = Posts.query.filter_by(user_id=user_id).all()
            
            posts_data = []
            for p in posts:
                likeCount = len(Likes.query.filter_by(post_id=p.id).all())

                post_data = {
                    "id": p.id,
                    "user_id": p.user_id,
                    "username": user.username,
                    "photo": "/api/v1/postuploads/{}".format(p.photo),
                    "caption": p.caption, 
                    "created_on": p.created_on,  
                    "likes": likeCount
                }
                posts_data.append(post_data)

            data = {
                "id": user.id,
                "username": user.username,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "location": user.location,
                "biography": user.biography,
                "profile_photo": "/api/v1/postuploads/{}".format(user.profile_photo),
                "joined_on": user.created_on,
                "posts": posts_data  
            }
            return jsonify(data)
        
        except Exception as e:
            # Handle any exceptions here
            error_message = {'error': 'An error occurred', 'details': str(e)}
            return jsonify(error_message), 500



#Endpoint for adding posts to users feed
#remember to add login required for this 

@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
#@jwt_required()  # This decorator requires JWT authentication
#@login_required
def add_post(user_id):
    pform = PostForm()

    if request.method == 'POST':
        try:
            #user_id = current_user.get_id()
            print("user id is", user_id)
            #current_user = get_jwt_identity()  # Get the current user from the JWT token


            if pform.validate_on_submit():

                #us_id = user_id
                p_caption = pform.caption.data
                p_photo = pform.photo.data
                created_on = datetime.datetime.now()

                filename = secure_filename(p_photo.filename)
                p_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                post = Posts(p_caption, filename, user_id)
                db.session.add(post)
                db.session.commit()

                return jsonify({
                        "message": "Post Successfully added",
                        "user_id": post.user_id,
                        "photo": post.photo,
                        "caption": post.caption
                })
            else:
                print("not validate")
                return jsonify({'errors': form_errors(pform)})
        except Exception as e:
        # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)
    print("not post")
    return jsonify({'errors': form_errors(pform)})
                    
 
            

#Endpoint for returning users posts
@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
#@jwt_required()  # This decorator requires JWT authentication
def posts(user_id):
    if request.method == 'GET':
        try:
            posts_all = Posts.query.filter_by(user_id=user_id).all() 
            user = Users.query.filter_by(id=user_id).first()

            posts_lst = []
            for p in posts_all:
                likeCount = len(Likes.query.filter_by(post_id=p.id).all())

                posts = {
                    "id": p.id,
                    "user_id": p.user_id,
                    "username": user.username,
                    "photo": "/api/v1/postuploads/{}".format(p.photo),
                    "caption": p.caption, 
                    "created_on": p.created_on, 
                    "likes": likeCount
                }
                posts_lst.append(posts)

            return jsonify({'posts': posts_lst})

        except Exception as e:
            # Return an error response
            return jsonify({'error': str(e)}), 500

            


#endpoint for returnung all posts

@app.route('/api/v1/posts', methods=['GET'])
#@jwt_required()  # This decorator requires JWT authentication
def allPosts():

    if request.method == 'GET':

        try:
            posts = Posts.query.all()
            postLst = []

            for post in posts:
                user = Users.query.filter_by(id=post.user_id).first()
                likes = Likes.query.filter_by(post_id=post.id).all()
                likes_lst = [{"user_id": like.user_id, "post_id": like.post_id} for like in likes]
                postLst.append({
                    "id": post.id,
                    "user_id": post.user_id,
                    "user_photo": "/api/v1/postuploads/{}".format(user.profile_photo),
                    "username": user.username,
                    "photo": "/api/v1/postuploads/{}".format(post.photo),
                    "caption": post.caption,
                    "created_on": post.created_on,
                    "likes": likes_lst
                })
            
            data = {"posts": postLst}
            return jsonify(data)
        
        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)




#endpoint for creating a follower relationship between current & target user 
            
@app.route('/api/v1/users/<target_id>/follow', methods=['POST'])
@jwt_required()  # This decorator requires JWT authentication
def follow(target_id):
    if request.method == 'POST':
        try:
            form = FollowForm()
            tar_user = Users.get_username(target_id)
    
            user_id = form.user_id.data

            if target_id == user_id:
                return jsonify({'message': "You cannot follow your self"})

            follow = Follows.query.filter_by(user_id=user_id, target_id=target_id).first()
            if follow != None:
                return jsonify({'message' : "You are already following this user"})

            follow = Follows(target_id, user_id)
            db.session.add(follow)
            db.session.commit()

            return jsonify({'message' : f" Now following {tar_user}"})

        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)


#Endpoint for retrieving the number of followers

@app.route('/api/v1/users/<user_id>/follow', methods=['GET'])
@jwt_required()  # This decorator requires JWT authentication
def getFollowers(user_id):
    
    if request.method == 'GET':

        try:
        
            # count = 0
        
            followers = Follows.query.filter_by(follower_id=user_id).all()
            followersLst = []

            for follow in followers:
                # count += 1
                followersLst.append(follow.user_id)
                 
            return jsonify({"followers": followersLst})
        
        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)


#Endpoint for Set a like on the current Post by the logged in User

@app.route('/api/v1/posts/<postID>/like', methods = ['POST'])
@jwt_required()  # This decorator requires JWT authentication
def like(postID):

    if request.method == 'POST':
        try:
            
            user_id = current_user.id
            post_id = postID
            
            like= Likes(post_id, user_id)
            
            #  add like to database
            
            db.session.add(like)
            db.session.commit()

            return jsonify({'message': 'Successfully liked post'})
        
        
        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)



    
#endpoint for getting post by name

@app.route("/api/v1/postuploads/<filename>", methods=['GET'])
def get_post(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename)


#endpoint for csrf token

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})



# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()





###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404