from flask import Blueprint, render_template, session,abort
import uuid
from ..model_dir.people import People, Follow, Like
from flask import jsonify, request, abort
from .. import db
app_file_social = Blueprint('social',__name__)


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


@app_file_social.route('/follow', methods=['POST'])
def create_follow():
    if not request.json:
        print("not json")
        abort(400)
    if not 'people_id' in request.json:
        print("miss people_id parameter")
        abort(400)
    if not 'followed_people_id' in request.json:
        print("miss followed_people_id parameter")
        abort(400)
    people_id           = request.json.get('people_id')
    followed_people_id  = request.json.get('followed_people_id')
    
    people          = getByIdOrByName(obj=People, id=people_id)
    people_followed = getByIdOrByName(obj=People, id=followed_people_id)

    if people is None:
        print("people is not found")
        abort(400)

    if people_followed is None:
        print("people_followed is not found")
        abort(400)

    follow = Follow( people_id = people.id, followed_people_id=people_followed.id )
    db.session.add(follow)
    db.session.commit() 
    return jsonify(follow.to_json())


@app_file_social.route("/follow/list", methods=["GET"])
def get_follows():
    follows = Follow.query.all()
    return jsonify([follow.to_json() for follow in follows])



@app_file_social.route('/like', methods=['POST'])
def create_like():
    if not request.json:
        print("not json")
        abort(400)
    if not 'people_id' in request.json:
        print("miss people_id parameter")
        abort(400)
    if not 'liked_people_id' in request.json:
        print("miss liked_people_id parameter")
        abort(400)
    people_id       = request.json.get('people_id')
    liked_people_id = request.json.get('liked_people_id')
    
 
    people          =  getByIdOrByName(obj=People, id=people_id)
    people_liked    =  getByIdOrByName(obj=People, id=liked_people_id)

    if people is None:
        print("people is not found")
        abort(400)

    if people_liked is None:
        print("people is not found")
        abort(400)


    like = Like( people_id = people.id, liked_people_id=people_liked.id )
    db.session.add(like)
    db.session.commit() 
    return jsonify(like.to_json())


@app_file_social.route("/like/list", methods=["GET"])
def get_like():
    likes = Like.query.all()
    return jsonify([item.to_json() for item in likes])

