from .. import db
from .profile import Profile
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


# file upload is here : https://www.youtube.com/watch?v=zMhmZ_ePGiM

class Media(db.Model, MyMixin):
    __tablename__ = 'medias'
    
    filename= db.Column(db.String(255), unique=True)
    width=db.Column(db.BigInteger)
    height=db.Column(db.BigInteger)
    filetype=db.Column(db.String(255))
    
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'filename': self.filename,
            'width': self.width,
            'height': self.height,
            'filetype': self.filetype
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'width': self.width,
            'height': self.height,
            'filetype': self.filetype
            
        }


class Gallery(db.Model, MyMixin):
    __tablename__ = 'galleries'
    profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    
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
            if ('all' in word) or 'profile' in word:
                result['profile'] =  self.profile.to_json() # backref from Profile
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

from sqlalchemy import event
@event.listens_for(Gallery, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    

@event.listens_for(Video, 'before_insert')
def do_stuff2(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Picture, 'before_insert')
def do_stuff3(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Media, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
