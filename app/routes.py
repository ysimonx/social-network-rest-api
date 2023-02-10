import os
import uuid
import datetime
import logging

from . import db
from . import create_app

from .model_dir.people import People, Follow, Like
from .model_dir.gallery import Gallery, Picture, Video
from .model_dir.meeting import Meeting, Country, Region, City, Address, Tour
from .model_dir.user import User, Subscription

from .route_dir.user import app_file_user
from .route_dir.subscription import app_file_subscription
from .route_dir.social import app_file_social
from .route_dir.gallery import app_file_gallery
from .route_dir.people import app_file_people
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
app.register_blueprint(app_file_people,         url_prefix=url_prefix)
app.register_blueprint(app_file_user,           url_prefix=url_prefix)
app.register_blueprint(app_file_subscription,   url_prefix=url_prefix)
app.register_blueprint(app_file_social,         url_prefix=url_prefix)
app.register_blueprint(app_file_gallery,        url_prefix=url_prefix)
app.register_blueprint(app_file_meeting,        url_prefix=url_prefix)

def getByIdOrByName(obj, id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.name==id).first()
    return result

def getByIdOrEmail(obj, id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.email==id).first()
    return result

 
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

# cf : https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
# https://flask-jwt-extended.readthedocs.io/en/stable/api/?highlight=get_jwt_identity#verify-tokens-in-request
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user =    getByIdOrEmail(obj=User,  id=email)
    
    if user is None:
        abort(401)
        
    result_check = user.check_password(password)
    if not result_check:
        abort(401)
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, result_check=result_check)

