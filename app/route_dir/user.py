from flask import Blueprint, render_template, session,abort
from ..model_dir.user import User, Subscription
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_user = Blueprint('user',__name__)


# cf : https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
# https://flask-jwt-extended.readthedocs.io/en/stable/api/?highlight=get_jwt_identity#verify-tokens-in-request
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app_file_user.route("/login", methods=["POST"])
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


@app_file_user.route("/user", methods=["GET"])
def get_user_list():
    items = User.query.all()
    return jsonify([item.to_json() for item in items])




# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/user
@app_file_user.route('/user', methods=['POST'])
def create_user():
    if not request.json:
        print("not json")
        abort(400)

    user = User(
        email=request.json.get('email'),
        password = request.json.get('password')
    )

    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201