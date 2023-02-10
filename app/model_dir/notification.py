from .. import db
from .mymixin import MyMixin
from .user import User
from sqlalchemy.orm import declarative_base, relationship, backref

import uuid


class Event(db.Model, MyMixin):
    __tablename__ = 'events'
    who =   db.Column(db.String(100), nullable=False)
    what =  db.Column(db.String(100), nullable=False)
    when =  db.Column(db.Datetime, nullable=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'who': self.who,
            'what': self.what,
            'when': self.when,
            '_internal' : self.get_internal(),       
        }


class Notification(db.Model, MyMixin):
    __tablename__ = 'notifications'
    event_id = db.Column(db.String(36), db.ForeignKey(Event.id))

    event = relationship('Event', backref="notifications")
    
    def to_json(self):
        return {
            'id': self.id,
            'event': self.event.to_json(),      
            '_internal' : self.get_internal(),
             
        }



class NotificationUsers(db.Model, MyMixin):
    __tablename__ = 'notifications_users'
    user_id       = db.Column(db.String(36), db.ForeignKey(User.id))
    notification_id = db.Column(db.String(36), db.ForeignKey(Notification.id))
    
    notification = relationship('People')
    user = relationship('User')
    
    def to_json(self):
        return {
            'id':                   self.id,
            '_internal' :           self.get_internal(),
            'notification_id' :     self.notification_id,
            'user_id':              self.user_id,
            'user':                 self.user.to_json(),
            'notification_id':      self.notification_id
        }

    




