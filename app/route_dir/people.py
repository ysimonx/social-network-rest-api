from flask import Blueprint, render_template, session,abort
import uuid
from ..model_dir.people import People
from flask import jsonify, request, abort
from .. import db
app_file_people = Blueprint('people',__name__)


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



# curl http://localhost:5000/people

@app_file_people.route("/people", methods=["GET"])
# @jwt_required()
def get_peoples():
    #current_user = get_jwt_identity()
    append_to_response =  request.args.get("append_to_response")
    peoples = People.query.all()
    if append_to_response is None:
        return jsonify([people.to_json() for people in peoples])
    else:
        return jsonify([people.to_json_append_to_response(append_to_response) for people in peoples])



@app_file_people.route("/people/<id_or_name>", methods=["GET"])
def get_people(id_or_name):
    people = getByIdOrByName(obj=People, id=id_or_name)
    append_to_response =  request.args.get("append_to_response")
    if people is None:
        abort(404)
    if append_to_response is None:
        return jsonify(people.to_json())
    else:
        return jsonify(people.to_json_append_to_response(append_to_response))


# curl http://localhost:5000/people/bab3097c-1804-4bdb-9675-ed8ab7b96b0c -X DELETE
@app_file_people.route("/people/<id_or_name>", methods=["DELETE"])
def delete_people(id_or_name):
    people = getByIdOrByName(obj=People, id=id_or_name)
    if people is None:
        abort(404)
    db.session.delete(people)
    db.session.commit()
    return jsonify({'result': True, 'id': id_or_name})

# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/people
@app_file_people.route('/people', methods=['POST'])
def create_people():
    if not request.json:
        print("not json")
        abort(400)

    people = People(
        name=request.json.get('name'),
    )
    db.session.add(people)
    db.session.commit()
    return jsonify(people.to_json()), 201


@app_file_people.route('/people/<id_or_name>', methods=['PUT'])
def update_people(id_or_name):
    if not request.json:
        abort(400)
    people = getByIdOrByName(obj=People, id=id_or_name)
    if people is None:
        abort(404)
    people.name = request.json.get('name', people.name)
    db.session.commit()
    return jsonify(people.to_json())
