from .. import db
from .profile import Profile
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Platform(db.Model, MyMixin):
    __tablename__ = 'platforms'



    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
        }
        


    def to_json_append_to_response(self, append_to_response):
        result = self.to_json()
      
        return result

      
from sqlalchemy import event
@event.listens_for(Platform, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
 