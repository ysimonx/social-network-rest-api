from .. import db
from .people import People
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM

class Gallery(db.Model, MyMixin):
    __tablename__ = 'galleries'
    people_id = db.Column(db.String(36), db.ForeignKey(People.id))
    
    pictures = relationship("Picture", cascade="all, delete", backref=backref("gallery",lazy="joined"))
    videos = relationship("Video", cascade="all, delete",  backref=backref("gallery",lazy="joined"))

    
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
        }
        


    def to_json_append_to_response(self, append_to_response):
        result = self.to_json()
        for word in append_to_response.split(','):
            if ('all' in word) or 'pictures' in word :
                result['pictures'] = [picture.to_json() for picture in self.pictures]
            if ('all' in word) or 'videos' in word :
                result['videos'] =  [video.to_json() for video in self.videos]
            if ('all' in word) or 'people' in word:
                result['people'] =  self.people.to_json() # backref from People
        return result


class Picture(db.Model, MyMixin):
    __tablename__ = 'pictures'
    gallery_id = db.Column(db.String(36), db.ForeignKey(Gallery.id))
    filename= db.Column(db.String(255), unique=True)
    size=db.Column(db.BigInteger)
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'filename': self.filename,
            'size': self.size
        }


class Video(db.Model, MyMixin):
    __tablename__ = 'videos'
    gallery_id = db.Column(db.String(36), db.ForeignKey(Gallery.id))
    filename= db.Column(db.String(255), unique=True)
    size=db.Column(db.BigInteger)
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'filename': self.filename,
            'size': self.size
        }

