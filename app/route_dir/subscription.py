from flask import Blueprint, render_template, session,abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..model_dir.user import User, Subscription
from ..model_dir.profile import Profile
from flask import jsonify, request, abort
from .. import db, getByIdOrByName, getByIdOrEmail
app_file_subscription = Blueprint('subscription',__name__)



@app_file_subscription.route('/subscription', methods=['POST'])
@jwt_required()
def create_subscription():
    if not request.json:
        print("not json")
        abort(400)
    if not 'profile_id' in request.json:
        print("miss profile_id parameter")
        abort(400)
    if not 'user_id' in request.json:
        print("miss user_id parameter")
        abort(400)
    profile_id       = request.json.get('profile_id')
    user_id         = request.json.get('user_id')
    
 
    profile =  getByIdOrByName(obj=Profile, id=profile_id)
    user =    getByIdOrEmail(obj=User,  id=user_id)

    if profile is None:
        print("profile is not found")
        abort(400)

    if user is None:
        print("user is not found")
        abort(400)


    subscription = Subscription( profile_id = profile.id, user_id=user.id )
    try:
        db.session.add(subscription)
        db.session.commit() 
    except exc.IntegrityError:
        abort(400)
    return jsonify(subscription.to_json())


@app_file_subscription.route("/subscription/list", methods=["GET"])
def get_subscription():
    items = Subscription.query.all()
    return jsonify([item.to_json() for item in items])

