from .. import db
from .mymixin import MyMixin
from sqlalchemy.orm import declarative_base, relationship, backref

import uuid

# TODO : https://stackoverflow.com/questions/1889251/sqlalchemy-many-to-many-relationship-on-a-single-table

class People(db.Model, MyMixin):
    __tablename__ = 'peoples'
    name = db.Column(db.String(255), unique=True, nullable=False)
    
    galleries   = relationship("Gallery",   
                                    cascade="all, delete", 
                                    backref=backref("people",lazy="joined")
                                    )
    

    is_liking   = relationship("People",
                                    cascade="all, delete",
                                    secondary = "likes", 
                                    primaryjoin="People.id == Like.people_id",
                                    secondaryjoin="People.id == Like.liked_people_id",
                                    backref="is_liked_by",
                                    viewonly=True
                                    )
    
    
    followers   = relationship("People",
                                    cascade="all, delete",
                                    secondary = "followings", 
                                    primaryjoin="People.id == Follow.followed_people_id",
                                    secondaryjoin="People.id == Follow.people_id",
                                    backref="is_following",
                                    viewonly=True
                                    )
    
    favorites   = relationship("People",
                                    cascade="all, delete",
                                    secondary = "favorites", 
                                    primaryjoin="People.id == Favorite.favorited_people_id",
                                    secondaryjoin="People.id == Favorite.people_id",
                                    viewonly=True
                                    )

    tours           = relationship("Tour",
                                    cascade="all, delete",
                                    back_populates="people"
                                    )

    reviews         = relationship("Review",
                                    cascade="all, delete",
                                    back_populates="people"
                                    )

    people_subscriptions = db.relationship("User", secondary="subscriptions", viewonly=True, lazy="select")


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
            'is_liking' : [{"people": item.to_json_light()} for item in self.is_liking],
            'is_liked_by': [{"people": item.to_json_light()} for item in self.is_liked_by],             
            'followers' : [{"people": item.to_json_light()} for item in self.followers],
            'is_following' : [{"people": item.to_json_light()} for item in self.is_following],
            'favorites'     : [{"people": item.to_json()}   for item    in self.favorites],         
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
                result['tours']         = [tour.to_json()   for tour    in self.tours]
                
            if b_all or  ('reviews' in word):
                result['reviews']       = [item.to_json()   for item    in self.reviews]
                
            if b_all or ('subscriptions' in word):
                result['subscriptions'] = [{"user": item.to_json_anonymous()}   for item    in self.people_subscriptions]

        return result;

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            '_internal' : self.get_internal()
        }
    

    


class Like(db.Model, MyMixin):
    __tablename__ = 'likes'
    people_id = db.Column(db.String(36), db.ForeignKey(People.id))
    liked_people_id = db.Column(db.String(36), db.ForeignKey(People.id))
    __table_args__ = (db.UniqueConstraint('people_id', 'liked_people_id', name='people_liked_uid'),)
    


    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'people_id':                self.people_id,
            'liked_people_id':          self.liked_people_id
        }

   


class Follow(db.Model, MyMixin):
    __tablename__ = 'followings'
    people_id = db.Column(db.String(36), db.ForeignKey(People.id))
    followed_people_id = db.Column(db.String(36),
                                    db.ForeignKey(People.id)
                                    )

    __table_args__ = (db.UniqueConstraint('people_id', 'followed_people_id', name='people_followed_uid'),)
    
                                    
    
    def to_json(self):
        return {
            'id':                       self.id,
            '_internal' :               self.get_internal(),
            'people_id':                self.people_id,
            'followed_people_id':      self. followed_people_id,
            
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
    people_id           = db.Column(db.String(36), db.ForeignKey(People.id))
    favorited_people_id = db.Column(db.String(36), db.ForeignKey(People.id))

    __table_args__ = (db.UniqueConstraint('people_id', 'favorited_people_id', name='people_favorite_uid'),)
    
    
   
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal()
        }


