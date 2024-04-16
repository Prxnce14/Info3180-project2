import os
from app import app, db
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Posts, Users, Likes
from app.forms import PostForm
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#Endpoint 

@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
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
    

@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
def add_post(user_id):

    if request.method == 'POST':
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

@app.route("/api/v1/postuploads/<filename>", methods=['GET'])
def get_post(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename)

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