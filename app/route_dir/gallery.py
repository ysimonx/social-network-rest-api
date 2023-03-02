from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from ..model_dir.profile import Profile
from ..model_dir.gallery import Gallery, Picture, Video, Media
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_gallery = Blueprint('gallery',__name__)

import cv2

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}





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




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[0].lower()


def get_user_path(user):
    path = os.path.abspath(
                    "app/" + 
                    os.path.join(
                        current_app.config['UPLOAD_FOLDER'],
                        MEDIA_DIR            
                    )
            )
    if (not os.path.exists(path)):
                mode = 0o755
                os.mkdir(path, mode)
                       
    path = os.path.abspath(
                    "app/" + 
                    os.path.join(
                        current_app.config['UPLOAD_FOLDER'],
                        MEDIA_DIR,
                        user
                    )
            )
   
    if (not os.path.exists(path)):
                # mode
                mode = 0o755
                os.mkdir(path, mode)
                
    return path
               

MEDIA_DIR = "media"

def crop_square(img, size, interpolation=cv2.INTER_AREA):
    h, w = img.shape[:2]
    min_size = numpy.amin([h,w])

    # Centralize and crop
    crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
    resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

    return resized

@app_file_gallery.route('/static/media/<user_id>/<name>')
def download_file(user_id, name):
    path = current_app.config["UPLOAD_FOLDER"] + "/media/" + user_id 
    print(path)
    return send_from_directory(path, name)
   
   
@app_file_gallery.route('/media/', methods=['POST'])
@jwt_required()
def upload_file():
  
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            abort(400)
        
        current_user = get_jwt_identity()
        
       
        
        if file and allowed_file(file.filename):
            path = get_user_path(current_user)
            filename = secure_filename(file.filename)
            
            #read image file string data
            filestr = file.read()
            #convert string data to numpy array
            file_bytes = numpy.fromstring(filestr, numpy.uint8)
            # convert numpy array to image
            img = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR) 
            if img is None:
               abort(400, "not an image")
                
            img_square = crop_square(img, 100)
            
            # convert to jpeg file
            filename = remove_extension(filename)+ ".jpeg"
            filename_square = remove_extension(filename) + "_square.jpeg"
        
            cv2.imwrite(os.path.join(path,filename), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(os.path.join(path,filename_square), img_square, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
               
            height, width, channels = img.shape
                
            final_filename = current_app.config['UPLOAD_FOLDER']+ "/" + MEDIA_DIR + "/"+ current_user + "/" + str(filename)
            
            media = getByIdOrFilename(Media, final_filename)
            if media is None:
                media = Media( filename = final_filename, filetype = "jpg", width=width, height=height )
                db.session.add(media)
            else:
                media.width = width
                media.height = height
                media.filetype = "jpg"

            db.session.commit() 
            
            return jsonify(media.to_json()), 201
        
        abort(400)
        
   