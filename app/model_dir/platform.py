from .. import db
from .people import People
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

