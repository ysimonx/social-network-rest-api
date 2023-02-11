from flask import Blueprint, render_template, session,abort
import uuid
from ..model_dir.people import People
from ..model_dir.gallery import Gallery, Picture, Video
from flask import jsonify, request, abort
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
def delete_video(id):
    video = Video.query.get(id)
    if video is None:
        abort(404)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'result': True, 'id': id})



@app_file_gallery.route("/gallery", methods=["GET"])
def get_galleries():
    opt_people_id = request.args.get("people_id")
    append_to_response = request.args.get("append_to_response")
    if opt_people_id is None:
        galleries = Gallery.query.all()
    else:
        galleries = Gallery.query.filter(Gallery.people_id == opt_people_id)
        
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
def delete_gallery(id):
    gallery = Gallery.query.get(id)
    if gallery is None:
        abort(404)
    db.session.delete(gallery)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


# curl -H "Content-Type: application/json" -X POST -d '{"people_id": "072bda67-60da-414e-b7b3-26a4cd458fa5"}' http://localhost:5000/gallery
@app_file_gallery.route('/gallery', methods=['POST'])
def create_gallery():
    print("create_gallery")
    if not request.json:
        print("not json")
        abort(400)
    
    if not 'people_id' in request.json:
        print("miss people_id parameter")
        abort(400)
        
    people_id = request.json.get('people_id')
    people = getByIdOrByName(obj=People, id=people_id)
    if people is None:
        abort(404)
    gallery = Gallery( people_id = people.id )
    db.session.add(gallery)
    db.session.commit() 
    return jsonify(gallery.to_json()), 201



@app_file_gallery.route('/gallery/<id>', methods=['PUT'])
def update_gallery(id):
    if not request.json:
        abort(400)
    gallery = Gallery.query.get(id)
    if gallery is None:
        abort(404)
    db.session.commit()
    return jsonify(gallery.to_json())

