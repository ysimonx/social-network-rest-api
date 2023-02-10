from .. import db
from .mymixin import MyMixin
from .people import People
from flask_bcrypt import generate_password_hash, check_password_hash



# ToDo : essayer ca plutot https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935
class User(db.Model, MyMixin):
    __tablename__ = 'users'

    
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
    

    people_subscriptions = db.relationship("People", secondary="subscriptions", cascade="all, delete", viewonly=True, lazy="select")

    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'email': self.email,
            'password': self.password,
            'subscriptions': [item.to_json() for item    in self.people_subscriptions]
        }

    def to_json_light(self):
        return {
            'id': self.id,
            'email': self.email
        }
        
    def to_json_anonymous(self):
        return {
            'id': self.id,
        }


    def hash_password(self):
            self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
            return check_password_hash(self.password, password)




class Subscription(db.Model, MyMixin):

    __tablename__ = 'subscriptions'
    
    user_id   = db.Column(db.String(36), db.ForeignKey(User.id))
    people_id = db.Column(db.String(36), db.ForeignKey(People.id))

    __table_args__ = (db.UniqueConstraint('user_id', 'people_id', name='user_people_uid'),)
    
    people   = db.relationship("People")
    user     = db.relationship("User")                          

    
    def to_json(self):
        
        return {
            'id': self.id,
            '_internal' :   self.get_internal(),
            'user':         self.user.to_json_light(),
            'people':       self.people.to_json_light(),
            #'user':     self.user.to_json()  

        }


