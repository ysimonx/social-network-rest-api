from flask import Blueprint, render_template, session,abort
from ..model_dir.user import User, Subscription
from flask import jsonify, request, abort
from .. import db
app_file_subscription = Blueprint('subscription',__name__)



@app_file_subscription.route('/subscription', methods=['POST'])
def create_subscription():
    if not request.json:
        print("not json")
        abort(400)
    if not 'people_id' in request.json:
        print("miss people_id parameter")
        abort(400)
    if not 'user_id' in request.json:
        print("miss user_id parameter")
        abort(400)
    people_id       = request.json.get('people_id')
    user_id         = request.json.get('user_id')
    
 
    people =  getByIdOrByName(obj=People, id=people_id)
    user =    getByIdOrEmail(obj=User,  id=user_id)

    if people is None:
        print("people is not found")
        abort(400)

    if user is None:
        print("user is not found")
        abort(400)


    subscription = Subscription( people_id = people.id, user_id=user.id )
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

