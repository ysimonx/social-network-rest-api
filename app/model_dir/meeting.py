from .. import db
from sqlalchemy.orm import declarative_base, relationship, backref
from .profile import Profile
from .mymixin import MyMixin



class Country(db.Model, MyMixin):
    __tablename__ = 'countries'
    name   = db.Column(db.String(100), unique=True)
    
    regions   = relationship("Region",   
                                cascade="all, delete", 
                                backref=backref("country",lazy="joined")
                                )
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name, 
            '_internal' : self.get_internal(),
        }
        
    def to_json_with_details(self):
        return {
            'id': self.id,
            'name': self.name, 
            '_internal' : self.get_internal(),
            'regions': [{"region": item.to_json_with_details()} for item in self.regions],  
        }
    
    def to_json_with_details_ancestors_only(self):
         return {
            'id': self.id,
            'name': self.name, 
            '_internal' : self.get_internal(),
            
        }

class Region(db.Model, MyMixin):
    __tablename__ = 'region'
    name   = db.Column(db.String(100), unique=True)
    country_id = db.Column(db.String(36), db.ForeignKey(Country.id))
    
    cities   = relationship("City",   
                                cascade="all, delete", 
                                backref=backref("region",lazy="joined")
                                )
      
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name, 
            'country_id' : self.country_id,
            '_internal' : self.get_internal(),
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'name': self.name, 
        }
        
    def to_json_with_details(self):
          return {
            'id': self.id,
            'name': self.name, 
            'country_id' : self.country_id,
            'cities': [{"city": item.to_json()} for item in self.cities]
        }
        
    def to_json_with_details_ancestors_only(self):
          return {
            'id': self.id,
            'name': self.name, 
            'country': self.country.to_json_with_details_ancestors_only()
        }

class City(db.Model, MyMixin):
    __tablename__ = 'cities'
    name   = db.Column(db.String(100), unique=True)
    region_id = db.Column(db.String(36), db.ForeignKey(Region.id))
    tours       = relationship("Tour", back_populates="city")
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name, 
            'region_id' : self.region_id,
            '_internal' : self.get_internal()
        }
        
    
    def to_json_light(self):
        return {
            'id': self.id,
            'name': self.name, 
        }
    
    def to_json_with_details_ancestors_only(self):
        return {
            'id': self.id,
            'name': self.name, 
            'region': self.region.to_json_with_details_ancestors_only(),
        }
        
    def to_json_with_details(self):
         return {
            'id': self.id,
            'name': self.name, 
            'region': self.region.to_json_with_details(),
        }

class Address(db.Model, MyMixin):
    __tablename__ = 'addresses'
    name   = db.Column(db.String(100))
    city_id = db.Column(db.String(36), db.ForeignKey(City.id))
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name, 
            'city_id' : self.city_id,
            '_internal' : self.get_internal()
        }

class Tour(db.Model, MyMixin):
    __tablename__ = 'tours'
    city_id     = db.Column(db.String(36), db.ForeignKey(City.id))
    profile_id   = db.Column(db.String(36), db.ForeignKey(Profile.id))
    time_start  = db.Column(db.DateTime(timezone=True))
    time_end    = db.Column(db.DateTime(timezone=True))
    
    city        = relationship("City", back_populates="tours")
    profile      = relationship("Profile", back_populates="tours")
    
    def to_json(self):
        return {
            'id':           self.id,
            'city_id':      self.city_id,
            'profile_id':    self.profile_id,
            'time_start':   self.time_start,
            'time_end':     self.time_end,
            '_internal':    self.get_internal()
            
        }
        
    def to_json_with_details(self):
        result = self.to_json()
        result["profile"] = self.profile.to_json_light()
        result["city"]   = self.city.to_json_with_details_ancestors_only()
        return result

class Meeting(db.Model, MyMixin):
    __tablename__ = 'meetings'
    visitor_profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    host_profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    time_start = db.Column(db.DateTime(timezone=True))
    city_id = db.Column(db.String(36), db.ForeignKey(City.id))
    

    def to_json(self):
        return {
            'id': self.id,
            'visitor_profile_id': self.visitor_profile_id, 
            'host_profile_id': self.host_profile_id, 
            'city_id': self.city_id,
            'time_start': self.time_start,
            '_internal' : self.get_internal()
        }

class Review(db.Model, MyMixin):
    __tablename__ = 'reviews'
    meeting_id = db.Column(db.String(36), db.ForeignKey(Meeting.id))
    profile_id = db.Column(db.String(36), db.ForeignKey(Profile.id))
    profile      = relationship("Profile", back_populates="reviews")
    rate =  db.Column(db.Integer, default=0)
    up_vote   = db.Column(db.Integer, default=0)
    down_vote = db.Column(db.Integer, default=0)
    
    def to_json(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id, 
            'meeting_id': self.meeting_id,
            'rate': self.rate,
             '_internal' : self.get_internal(),
            
        }
        
        
from sqlalchemy import event
@event.listens_for(Country, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Region, 'before_insert')
def do_stuff2(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(City, 'before_insert')
def do_stuff3(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

@event.listens_for(Address, 'before_insert')
def do_stuff4(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Tour, 'before_insert')
def do_stuff5(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
@event.listens_for(Meeting, 'before_insert')
def do_stuff6(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

@event.listens_for(Review, 'before_insert')
def do_stuff6(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)

