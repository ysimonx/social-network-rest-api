from .. import db
from sqlalchemy import event
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from .mymixin import MyMixin
from sqlalchemy.orm import declarative_base, relationship, backref

import uuid

# TODO : https://stackoverflow.com/questions/1889251/sqlalchemy-many-to-many-relationship-on-a-single-table

class Profile(db.Model, MyMixin):
    __tablename__ = 'profiles'
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    galleries   = relationship("Gallery",   
                                    cascade="all, delete", 
                                    backref=backref("profile",lazy="joined")
                                    )
    

    is_liking   = relationship("Profile",
                                    cascade="all, delete",
                                    secondary = "likes", 
                                    primaryjoin="Profile.id == Like.profile_id",
                                    secondaryjoin="Profile.id == Like.liked_profile_id",
                                    backref="is_liked_by",
                                    viewonly=True
                                    )
    
    
    followers   = relationship("Profile",
                                    cascade="all, delete",
                                    secondary = "followings", 
                                    primaryjoin="Profile.id == Follow.followed_profile_id",
                                    secondaryjoin="Profile.id == Follow.profile_id",
                                    backref="is_following",
                                    viewonly=True
                                    )
    
    favorites   = relationship("Profile",
                                    cascade="all, delete",
                                    secondary = "favorites", 
                                    primaryjoin="Profile.id == Favorite.favorited_profile_id",
                                    secondaryjoin="Profile.id == Favorite.profile_id",
                                    viewonly=True
                                    )

    tours           = relationship("Tour",
                                    cascade="all, delete",
                                    back_populates="profile"
                                    )

    reviews         = relationship("Review",
                                    cascade="all, delete",
                                    back_populates="profile"
                                    )

    profile_subscriptions = db.relationship("User", secondary="subscriptions", viewonly=True, lazy="select")


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            '_internal' : self.get_internal()
        }
    
    def to_json_light(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def to_json_social_network(self):
       
        return {
            'is_liking' : [{"profile": item.to_json_light()} for item in self.is_liking],
            'is_liked_by': [{"profile": item.to_json_light()} for item in self.is_liked_by],             
            'followers' : [{"profile": item.to_json_light()} for item in self.followers],
            'is_following' : [{"profile": item.to_json_light()} for item in self.is_following],
            'favorites'     : [{"profile": item.to_json()}   for item    in self.favorites],         
        }
        
        
    def to_json_append_to_response(self, append_to_response):
        result = self.to_json()
        
        b_all = False
        if ('all' == append_to_response):
            b_all = True
            
        for word in append_to_response.split(','):
            if b_all or ('galleries' in word):
                result['galleries'] = [gallery.to_json_append_to_response(append_to_response)  for gallery in self.galleries]
            
            if b_all or ('social_network' in word):
                result['social_network'] = self.to_json_social_network()
            
            if b_all or  ('tours' in word):
                result['tours']         = [tour.to_json_with_details()   for tour    in self.tours]
                
            if b_all or  ('reviews' in word):
                result['reviews']       = [item.to_json()   for item    in self.reviews]
                
            if b_all or ('subscriptions' in word):
                result['subscriptions'] = [{"user": item.to_json_anonymous()}   for item    in self.profile_subscriptions]

        return result;

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            '_internal' : self.get_internal()
        }

class Like(db.Model, MyMixin):
    __tablename__ = 'likes'
    profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    liked_profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    __table_args__ = (db.UniqueConstraint('profile_id', 'liked_profile_id', name='profile_liked_uid'),)
    


    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'profile_id':                self.profile_id,
            'liked_profile_id':          self.liked_profile_id
        }

class Follow(db.Model, MyMixin):
    __tablename__ = 'followings'
    profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    followed_profile_id = db.Column(db.String(36),
                                    db.ForeignKey(Profile.id)
                                    )

    __table_args__ = (db.UniqueConstraint('profile_id', 'followed_profile_id', name='profile_followed_uid'),)
    
                                    
    
    def to_json(self):
        return {
            'id':                       self.id,
            '_internal' :               self.get_internal(),
            'profile_id':                self.profile_id,
            'followed_profile_id':      self. followed_profile_id,
            
        }

    def to_json_followers(self):
        return {
            '_internal' :               self.get_internal(),
           
        }

    def to_json_followings(self):
         return {
            '_internal' :               self.get_internal(),
            
        }

class Favorite(db.Model, MyMixin):
    __tablename__ = 'favorites'
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    profile_id           = db.Column(db.String(36), db.ForeignKey(Profile.id))
    favorited_profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))

    __table_args__ = (db.UniqueConstraint('profile_id', 'favorited_profile_id', name='profile_favorite_uid'),)
    
    
   
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal()
        }
        
@event.listens_for(Profile, 'before_insert')
def do_stuff(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Like, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Follow, 'before_insert')
def do_stuff2(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Favorite, 'before_insert')
def do_stuff3(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
