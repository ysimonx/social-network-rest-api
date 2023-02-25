from flask import Blueprint, render_template, session,abort
import uuid
from ..model_dir.profile import Profile
from ..model_dir.gallery import Gallery, Picture, Video
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


from .. import db,  getByIdOrByName
app_file_gallery = Blueprint('gallery',__name__)





# cf fileupload : https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

@app_file_gallery.route("/picture", methods=["GET"])
def get_pictures():
    pictures = Picture.query.all()
    return jsonify([picture.to_json() for picture in pictures])


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM
# flutter image upload exemple : https://www.youtube.com/watch?v=dsPdIdrgAD4
@app_file_gallery.route('/picture', methods=['POST'])
@jwt_required()
def create_picture():
    if not request.json:
        print("not json")
        abort(400)
    if not 'gallery_id' in request.json:
        print("miss gallery_id parameter")
        abort(400)
    if not 'filename' in request.json:
        print("miss filename parameter")
        abort(400)
            
    gallery_id = request.json.get('gallery_id')
    filename = request.json.get('filename')

    picture = Picture( gallery_id = gallery_id, filename=filename )
    db.session.add(picture)
    db.session.commit() 
    return jsonify(picture.to_json()), 201

@app_file_gallery.route("/picture/<id>", methods=["GET"])
def get_picture(id):
    picture = Picture.query.get(id)
    if picture is None:
        abort(404)
    return jsonify(picture.to_json_to_root())

@app_file_gallery.route('/picture/<id>', methods=['PUT'])
@jwt_required()
def update_picture(id):
    if not request.json:
        abort(400)
    picture = Picture.query.get(id)
    if picture is None:
        abort(404)
    picture.filename = request.json.get('name', picture.filename)
    db.session.commit()
    return jsonify(picture.to_json())

@app_file_gallery.route("/picture/<id>", methods=["DELETE"])
@jwt_required()
def delete_picture(id):
    picture = Picture.query.get(id)
    if picture is None:
        abort(404)
    db.session.delete(picture)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


@app_file_gallery.route("/video", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_json() for video in videos])

# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM

@app_file_gallery.route('/video', methods=['POST'])
@jwt_required()
def create_video():
    if not request.json:
        print("not json")
        abort(400)
    if not 'gallery_id' in request.json:
        print("miss gallery_id parameter")
        abort(400)
    if not 'filename' in request.json:
        print("miss filename parameter")
        abort(400)    
    gallery_id = request.json.get('gallery_id')
    filename   = request.json.get('filename')
    
    video = Video( gallery_id = gallery_id, filename=filename )
    db.session.add(video)
    db.session.commit() 
    return jsonify(video.to_json()), 201

@app_file_gallery.route("/video/<id>", methods=["GET"])
def get_video(id):
    video = Video.query.get(id)
    if video is None:
        abort(404)
    return jsonify(video.to_json())

@app_file_gallery.route('/video/<id>', methods=['PUT'])
@jwt_required()
def update_video(id):
    if not request.json:
        abort(400)
    video = Video.query.get(id)
    if video is None:
        abort(404)
    video.filename = request.json.get('name', video.filename)
    db.session.commit()
    return jsonify(video.to_json())

@app_file_gallery.route("/video/<id>", methods=["DELETE"])
@jwt_required()
def delete_video(id):
    video = Video.query.get(id)
    if video is None:
        abort(404)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'result': True, 'id': id})



@app_file_gallery.route("/gallery", methods=["GET"])
def get_galleries():
    opt_profile_id = request.args.get("profile_id")
    append_to_response = request.args.get("append_to_response")
    if opt_profile_id is None:
        galleries = Gallery.query.all()
    else:
        galleries = Gallery.query.filter(Gallery.profile_id == opt_profile_id)
        
    if append_to_response is None:
        return jsonify([gallery.to_json() for gallery in galleries])
    else:
         return jsonify([gallery.to_json_append_to_response(append_to_response) for gallery in galleries])


@app_file_gallery.route("/gallery/<id>", methods=["GET"])
def get_gallery(id):
    gallery = Gallery.query.get(id)
    if gallery is None:
        abort(404)
    return jsonify(gallery.to_json())


@app_file_gallery.route("/gallery/<id>", methods=["DELETE"])
@jwt_required()
def delete_gallery(id):
    gallery = Gallery.query.get(id)
    if gallery is None:
        abort(404)
    db.session.delete(gallery)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


# curl -H "Content-Type: application/json" -X POST -d '{"profile_id": "072bda67-60da-414e-b7b3-26a4cd458fa5"}' http://localhost:5000/gallery
@app_file_gallery.route('/gallery', methods=['POST'])
@jwt_required()
def create_gallery():
    print("create_gallery")
    if not request.json:
        print("not json")
        abort(400)
    
    if not 'profile_id' in request.json:
        print("miss profile_id parameter")
        abort(400)
        
    profile_id = request.json.get('profile_id')
    profile = getByIdOrByName(obj=Profile, id=profile_id)
    if profile is None:
        abort(404)
    gallery = Gallery( profile_id = profile.id )
    db.session.add(gallery)
    db.session.commit() 
    return jsonify(gallery.to_json()), 201



@app_file_gallery.route('/gallery/<id>', methods=['PUT'])
@jwt_required()
def update_gallery(id):
    if not request.json:
        abort(400)
    gallery = Gallery.query.get(id)
    if gallery is None:
        abort(404)
    db.session.commit()
    return jsonify(gallery.to_json())



