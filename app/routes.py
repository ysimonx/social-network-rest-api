import os
import uuid
import datetime
import logging

from . import db, getByIdOrEmail, getByIdOrByName
from . import create_app

from .model_dir.profile import Profile, Follow, Like
from .model_dir.gallery import Gallery, Picture, Video
from .model_dir.meeting import Meeting, Country, Region, City, Address, Tour
from .model_dir.user import User, Subscription

from .route_dir.user import app_file_user
from .route_dir.subscription import app_file_subscription
from .route_dir.social import app_file_social
from .route_dir.gallery import app_file_gallery
from .route_dir.profile import app_file_profile
from .route_dir.meeting import app_file_meeting

from sqlalchemy import exc
from flask import jsonify, request, abort
from flask_mail import Mail


# todo : implement https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['DEBUG'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Mail
# After 'Create app'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)

url_prefix = "/api/v1"
app.register_blueprint(app_file_profile,         url_prefix=url_prefix)
app.register_blueprint(app_file_user,           url_prefix=url_prefix)
app.register_blueprint(app_file_subscription,   url_prefix=url_prefix)
app.register_blueprint(app_file_social,         url_prefix=url_prefix)
app.register_blueprint(app_file_gallery,        url_prefix=url_prefix)
app.register_blueprint(app_file_meeting,        url_prefix=url_prefix)

 
@app.before_request
def before_request():
    app.logger.info("before_request")

@app.after_request
def after_request(response):
    # 
    app.logger.info("after_request")
    return response

@app.before_first_request
def before_first_request():
    log_level = logging.INFO
 
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
 
    app.logger.setLevel(log_level)


@app.route("/api/v1/init", methods=["GET"])
def init():
    db.drop_all()
    db.create_all()
    return "ok"


