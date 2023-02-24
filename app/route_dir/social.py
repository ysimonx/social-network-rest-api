from flask import Blueprint, render_template, session,abort
from flask_jwt_extended import jwt_required, get_jwt_identity

import uuid
from ..model_dir.profile import Profile, Follow, Like
from flask import jsonify, request, abort
from .. import db,   getByIdOrByName

app_file_social = Blueprint('social',__name__)


@app_file_social.route('/follow', methods=['POST'])
@jwt_required()
def create_follow():
    if not request.json:
        print("not json")
        abort(400)
    if not 'profile_id' in request.json:
        print("miss profile_id parameter")
        abort(400)
    if not 'followed_profile_id' in request.json:
        print("miss followed_profile_id parameter")
        abort(400)
    profile_id           = request.json.get('profile_id')
    followed_profile_id  = request.json.get('followed_profile_id')
    
    profile          = getByIdOrByName(obj=Profile, id=profile_id)
    profile_followed = getByIdOrByName(obj=Profile, id=followed_profile_id)

    if profile is None:
        print("profile is not found")
        abort(400)

    if profile_followed is None:
        print("profile_followed is not found")
        abort(400)

    follow = Follow( profile_id = profile.id, followed_profile_id=profile_followed.id )
    db.session.add(follow)
    db.session.commit() 
    return jsonify(follow.to_json())


@app_file_social.route("/follow/list", methods=["GET"])
def get_follows():
    follows = Follow.query.all()
    return jsonify([follow.to_json() for follow in follows])



@app_file_social.route('/like', methods=['POST'])
@jwt_required()
def create_like():
    if not request.json:
        print("not json")
        abort(400)
    if not 'profile_id' in request.json:
        print("miss profile_id parameter")
        abort(400)
    if not 'liked_profile_id' in request.json:
        print("miss liked_profile_id parameter")
        abort(400)
    profile_id       = request.json.get('profile_id')
    liked_profile_id = request.json.get('liked_profile_id')
    
 
    profile          =  getByIdOrByName(obj=Profile, id=profile_id)
    profile_liked    =  getByIdOrByName(obj=Profile, id=liked_profile_id)

    if profile is None:
        print("profile is not found")
        abort(400)

    if profile_liked is None:
        print("profile is not found")
        abort(400)


    like = Like( profile_id = profile.id, liked_profile_id=profile_liked.id )
    db.session.add(like)
    db.session.commit() 
    return jsonify(like.to_json())


@app_file_social.route("/like/list", methods=["GET"])
def get_like():
    likes = Like.query.all()
    return jsonify([item.to_json() for item in likes])

