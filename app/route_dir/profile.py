from flask import Blueprint, render_template, session,abort
import uuid
from ..model_dir.profile import Profile
from flask import jsonify, request, abort
from .. import db,   getByIdOrByName
from flask_jwt_extended import jwt_required, get_jwt_identity

app_file_profile = Blueprint('profile',__name__)


@app_file_profile.route("/profile", methods=["GET"])
# @jwt_required()
def get_profiles():
   
    append_to_response =  request.args.get("append_to_response")
    profiles = Profile.query.all()
    if append_to_response is None:
        return jsonify([profile.to_json() for profile in profiles])
    else:
        return jsonify([profile.to_json_append_to_response(append_to_response) for profile in profiles])



@app_file_profile.route("/profile/<id_or_name>", methods=["GET"])
def get_profile(id_or_name):
    profile = getByIdOrByName(obj=Profile, id=id_or_name)
    append_to_response =  request.args.get("append_to_response")
    if profile is None:
        abort(404)
    if append_to_response is None:
        return jsonify(profile.to_json())
    else:
        return jsonify(profile.to_json_append_to_response(append_to_response))


# curl http://localhost:5000/profile/bab3097c-1804-4bdb-9675-ed8ab7b96b0c -X DELETE
@app_file_profile.route("/profile/<id_or_name>", methods=["DELETE"])
@jwt_required()
def delete_profile(id_or_name):
    profile = getByIdOrByName(obj=Profile, id=id_or_name)
    if profile is None:
        abort(404)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'result': True, 'id': id_or_name})

# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/profile
@app_file_profile.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    if not request.json:
        print("not json")
        abort(400)

    profile = Profile(
        name=request.json.get('name'),
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.to_json()), 201


@app_file_profile.route('/profile/<id_or_name>', methods=['PUT'])
@jwt_required()
def update_profile(id_or_name):
    if not request.json:
        abort(400)
    profile = getByIdOrByName(obj=Profile, id=id_or_name)
    if profile is None:
        abort(404)
    profile.name = request.json.get('name', profile.name)
    db.session.commit()
    return jsonify(profile.to_json())
