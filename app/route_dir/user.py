from flask import Blueprint, render_template, session,abort
from ..model_dir.user import User, Subscription
from flask import jsonify, request, abort
from .. import db
app_file_user = Blueprint('user',__name__)


@app_file_user.route("/user/list", methods=["GET"])
def get_user_list():
    items = User.query.all()
    return jsonify([item.to_json() for item in items])




# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/people
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