import os
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Posts, Users, Likes, Follows
from app.forms import PostForm, LoginForm, UsersForm
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


###
# Routing for your application.
###

# @app.route('/')
# def index():
#     return jsonify(message="This is the beginning of our API")

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


#Endpoint for registering a user 

@app.route('/api/v1/register', methods=['POST'])
def create_user():
    
    if request.method == 'POST ':
        try:
            userform = UsersForm()
            if userform.validate_on_submit():

                uname = userform.uname.data
                pword = userform.password.data
                fname = userform.firstname.data
                lname = userform.lastname.data
                email = userform.email.data
                local = userform.location.data
                bio = userform.biography.data
                created_at = datetime.datetime.now()
                img = userform.photofile.data
                filename = secure_filename(img.filename)

                img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                new_user = Users(uname, pword, fname, lname, email, local, bio, filename, created_at)

                db.session.add(new_user)
                db.session.commit()

                flash('User Registered', 'success')

                return jsonify({
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
            flash({'An error occurred' : str(e)}, 400)


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

                    # Generate JWT token
                    access_token = create_access_token(identity=user)

                    # Remember to flash a message to the user
                    flash('Logged in successfully.', 'success')

                    # Return JWT token to the client
                
                    return redirect(url_for('explore',jsonify({'access_token': access_token}) ))
                        
                else:
                    flash('Username or Password is incorrect.', 'danger')

            else:
                    errors = form_errors(form)
                    return jsonify({'errors': errors})

        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)
            





@app.route('/api/v1/auth/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))



#Endpoint for adding posts to users feed
#remember to add login required for this 

@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@jwt_required()  # This decorator requires JWT authentication
def add_post(user_id):

    current_user = get_jwt_identity()  # Get the current user from the JWT token

    if current_user.get('user_id') != user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    if request.method == 'POST':
        try:
            pform = PostForm()

            if pform.validate_on_submit():

                us_id = user_id
                p_caption = pform.caption.data
                p_photo = pform.photo.data

                filename = secure_filename(p_photo.filename)
                p_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                post = Posts(caption=p_caption, photo=filename, user_id=us_id)
                db.session.add(post)
                db.session.commit()

                return jsonify({
                        "message": "Post Successfully added",
                        "user_id": post.user_id,
                        "photo": post.photo,
                        "caption": post.caption
                })

            else:
                return jsonify({'errors': form_errors(pform)})
            
        except Exception as e:
            # Handle any exceptions here
            flash({'An error occurred' : str(e)}, 400)
            

#Endpoint for returning users posts

@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@jwt_required()  # This decorator requires JWT authentication
def posts(user_id):
    if request.method == 'GET':
        
        posts_all = Posts.query.filter_by(user_id = user_id).all() 
        user = Users.query.filter_by(id=user_id).first()

        posts_lst =[]
        for p in posts_all:

            likeCount = len(Likes.query.filter_by(post_id=p.id).all())

            posts={
                "id": p.id,
                "user_id": p.user_id,
                "username": user.username, 
                "user_profile_photo": "/api/v1/postuploads/"+ user.profile_photo,
                "photo": "/api/v1/postuploads/"+ p.photo,
                "caption": p.caption, 
                "created_on": p.creatd_on, 
                "likes": likeCount
                }
            posts_lst.append(posts)
        return jsonify({'posts': posts_lst})
    


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