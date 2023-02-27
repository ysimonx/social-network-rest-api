import os
import logging

from app.model_dir.meeting import City, Country, Region

from . import db, getByIdOrEmail, getByIdOrByName
from . import create_app

from .route_dir.user import app_file_user
from .route_dir.subscription import app_file_subscription
from .route_dir.social import app_file_social
from .route_dir.gallery import app_file_gallery
from .route_dir.profile import app_file_profile
from .route_dir.meeting import app_file_meeting

from flask import jsonify, abort, render_template
from flask_mail import Mail
from flask_jwt_extended import JWTManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['DEBUG'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Setup upload folder
UPLOAD_FOLDER = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)

# Setup Routes
url_prefix = "/api/v1"
app.register_blueprint(app_file_profile,         url_prefix=url_prefix)
app.register_blueprint(app_file_user,           url_prefix=url_prefix)
app.register_blueprint(app_file_subscription,   url_prefix=url_prefix)
app.register_blueprint(app_file_social,         url_prefix=url_prefix)
app.register_blueprint(app_file_gallery,        url_prefix=url_prefix)
app.register_blueprint(app_file_meeting,        url_prefix=url_prefix)

 
@app.before_request
def before_request():
    app.logger.info("before_request")

@app.after_request
def after_request(response):
    app.logger.info("after_request")
    return response

# Setup log folder
@app.before_first_request
def before_first_request():

    populate_data()

    log_level = logging.INFO
 
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)



@app.route("/api/v1/init", methods=["GET"])
def init():
    db.drop_all()
    db.create_all()
    populate_data()

    return "ok"

@app.route("/api/v1/swagger-ui", methods=["GET"])
def swagger():
    return render_template('swagger.html')


def populate_data():
    data =  {
            "france": {
                "auvergne-rhône-alpes": {
                    "lyon": {},
                    "annecy": {}
                },
                "bourgogne-franche-comté": {
                    "besançon": {},
                    "dijon": {}
                },
                "bretagne": {
                    "rennes": {},
                    "st-malo": {}
                },
                "centre-val de loire": {
                    "orleans": {},
                    "tour": {}
                },
                "corse": {
                      "ajaccio": {},
                      "bastia": {},
                      "calvi": {},
                },
                "grand est": {
                    "strasbourg": {},
                    "reims": {},
                    "metz": {}
                },

                "île-de-france": {
                    "paris": {}        
                },
                "normandie": {
                    "caen": {},
                    "rouen": {}        
                },
                "nouvelle-aquitaine": {
                    "bordeaux": {}        
                },
                "occitanie": {
                    "toulouse": {}        
                },
                "pays de la loire": {
                    "angers": {}      ,
                    "nantes": {}      
                },
                "provence-alpes-côte d'azur": {
                    "aix-en-provence": {},
                    "marseille": {},

                },
                "hauts-de-france": {
                    "lille": {},
                    "roubaix": {}
                }
            }, 
    }
    for country, regions in data.items():
        print(country)
        _country = getByIdOrByName(obj=Country, id=country)
        if _country is None:
            _country = Country( name = country )
            db.session.add(_country)


            print(_country.to_json())

        
        for region, cities in regions.items():
            _region = getByIdOrByName(obj=Region, id=region)
            if _region is None:
                _region = Region( country_id = _country.id, name = region )
                db.session.add(_region)



            for city, details in cities.items():
                _city = getByIdOrByName(obj=City, id=city)
                if _city is None:
                    _city = City( region_id = _region.id,  name = city )
                    db.session.add(_city)


                print(country, region, city)
    print("fini")
    db.session.commit()