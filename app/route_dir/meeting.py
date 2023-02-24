from flask import Blueprint, render_template, session,abort
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from ..model_dir.meeting import Country, Region, City, Tour, Meeting
from ..model_dir.gallery import Gallery, Picture, Video
from ..model_dir.profile import Profile

from flask import jsonify, request, abort
from .. import db, getByIdOrByName
app_file_meeting = Blueprint('meeting',__name__)




@app_file_meeting.route("/country", methods=["GET"])
def get_countries():
    items = Country.query.all()
    
    append_to_response =  request.args.get("append_to_response")
    if append_to_response is None:
        return jsonify([item.to_json() for item in items])
    else:
        return jsonify([item.to_json_with_details() for item in items])


@app_file_meeting.route('/country', methods=['POST'])
@jwt_required()
def create_country():
    if not request.json:
        print("not json")
        abort(400)
    if not 'name' in request.json:
        print("miss name parameter")
        abort(400)
        
    name = request.json.get('name').lower()

    country = Country( name = name )
    db.session.add(country)
    db.session.commit() 
    return jsonify(country.to_json()), 201

@app_file_meeting.route("/country/<id_or_name>", methods=["GET"])
def get_country(id_or_name):
    country = getByIdOrByName(obj=Country, id=id_or_name)
    if country is None:
        abort(404)
    return jsonify(country.to_json())

@app_file_meeting.route('/country/<id_or_name>', methods=['PUT'])
def update_country(id_or_name):
    if not request.json:
        abort(400)
    country = getByIdOrByName(obj=Country, id=id_or_name)
    if country is None:
        abort(404)
    country.name = request.json.get('name', country.name).lower()
    db.session.commit()
    return jsonify(country.to_json())

@app_file_meeting.route("/country/<id_or_name>", methods=["DELETE"])
@jwt_required()
def delete_country(id_or_name):
    country = getByIdOrByName(obj=Country, id=id_or_name)
    if country is None:
        abort(404)
    db.session.delete(country)
    db.session.commit()
    return jsonify({'result': True, 'id': id_or_name})



@app_file_meeting.route("/region", methods=["GET"])
def get_regions():
    items = Region.query.all()
    append_to_response =  request.args.get("append_to_response")
    if append_to_response is None:
        return jsonify([item.to_json() for item in items])
    else:
        return jsonify([item.to_json_with_details() for item in items])

@app_file_meeting.route('/region', methods=['POST'])
@jwt_required()
def create_region():
    if not request.json:
        print("not json")
        abort(400)
        
    if not 'country_id' in request.json:
        print("miss country_id parameter")
        abort(400)
    
    if not 'name' in request.json:
        print("miss name parameter")
        abort(400)
        
    country_id = request.json.get('country_id')
    name = request.json.get('name').lower()

 
    country = getByIdOrByName(obj=Country, id=country_id)
    if country is None:
        abort(404, "country is not found")
        
    region = Region( country_id = country.id , name= name)
    db.session.add(region)
    db.session.commit() 
    return jsonify(region.to_json()), 201

@app_file_meeting.route("/region/<id>", methods=["GET"])
def get_region(id):
    region = getByIdOrByName(Region, id)
    if region is None:
        abort(404)
    return jsonify(region.to_json())

@app_file_meeting.route('/region/<id>', methods=['PUT'])
def update_region(id):
    if not request.json:
        abort(400)
    region = getByIdOrByName(Region, id)
    if region is None:
        abort(404)
    region.name = request.json.get('name', region.name).lower()
    db.session.commit()
    return jsonify(region.to_json())

@app_file_meeting.route("/region/<id>", methods=["DELETE"])
@jwt_required()
def delete_region(id):
    region = getByIdOrByName(Region, id)
    if region is None:
        abort(404)
    db.session.delete(region)
    db.session.commit()
    return jsonify({'result': True, 'id': id})



@app_file_meeting.route("/city", methods=["GET"])
def get_cities():
    items = City.query.all()
    return jsonify([item.to_json() for item in items])


@app_file_meeting.route('/city', methods=['POST'])
@jwt_required()
def create_city():
    if not request.json:
        print("not json")
        abort(400)
        
    if not 'region_id' in request.json:
        print("miss region_id parameter")
        abort(400)
    
    if not 'name' in request.json:
        print("miss name parameter")
        abort(400)
       
    region_id = request.json.get('region_id')
    name = request.json.get('name').lower()
    
    region = getByIdOrByName(obj=Region, id=region_id)
    if region is None:
        abort(404, "region not found")
        

    city = City( region_id = region.id , name= name)
    db.session.add(city)
    db.session.commit() 
    return jsonify(city.to_json()), 201

@app_file_meeting.route("/city/<id>", methods=["GET"])
def get_city(id):
    city = getByIdOrByName(City, id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())

@app_file_meeting.route('/city/<id>', methods=['PUT'])
def update_city(id):
    if not request.json:
        abort(400)
    city = getByIdOrByName(City, id)
    if city is None:
        abort(404)
    city.name = request.json.get('name', city.name).lower()
    db.session.commit()
    return jsonify(city.to_json())

@app_file_meeting.route("/city/<id>", methods=["DELETE"])
@jwt_required()
def delete_city(id):
    city = getByIdOrByName(City, id)
    if city is None:
        abort(404)
    db.session.delete(city)
    db.session.commit()
    return jsonify({'result': True, 'id': id})




@app_file_meeting.route("/tour", methods=["GET"])
def get_tours():
    tours = Tour.query.all()
    append_to_response =  request.args.get("append_to_response")
    if append_to_response is None:
        return jsonify([item.to_json() for item in tours])
    else:
        return jsonify([item.to_json_with_details() for item in tours])


@app_file_meeting.route("/tour/<id>", methods=["DELETE"])
@jwt_required()
def delete_tour(id):
    tour = Tour.query.get(id)
    if tour is None:
        abort(404)
    db.session.delete(tour)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


# 
# curl --request POST \
#  --url http://localhost:5000/api/v1/tour \
#  --header 'Content-Type: application/json' \
#  --data '{
#  "city_id": "Aix-en-provence",
#  "profile_id": "manue",
#  "time_start": "2023-01-01",
#  "time_end": "2023-02-01"
#  }'
# 
@app_file_meeting.route('/tour', methods=['POST'])
@jwt_required()
def create_tour():
    if not request.json:
        print("not json")
        abort(400)
        
    if not 'city_id' in request.json:
        print("miss city_id parameter")
        abort(400)
    
    if not 'profile_id' in request.json:
        print("miss profile_id parameter")
        abort(400)
    
    if not 'time_start' in request.json:
        print("miss time_start parameter")
        abort(400)
     
    if not 'time_end' in request.json:
        print("miss time_end parameter")
        abort(400)
          
    city_id     = request.json.get('city_id')
    profile_id   = request.json.get('profile_id')
    time_start  = request.json.get('time_start')
    time_end    = request.json.get('time_end')
    
    city        = getByIdOrByName(obj=City, id=city_id)
    profile      = getByIdOrByName(obj=Profile, id=profile_id)
    if city is None:
        abort(404, "city not found")
    if profile is None:
        abort(404, "profile not found")

    tour = Tour( city_id = city.id , profile_id= profile.id, time_start=time_start, time_end = time_end)

    db.session.add(tour)
    db.session.commit() 

    return jsonify(tour.to_json()), 201
