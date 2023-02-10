from .. import db

from sqlalchemy.orm import declarative_base, relationship, declared_attr
import uuid
from datetime import date, datetime

def formatted_date_iso(date):
    if date is None:
        return None
    return date.isoformat()
    

class MyMixin(object):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def get_internal(self):
        return {
                
                'time_created_utc': formatted_date_iso(self.time_created),
                'time_updated_utc': formatted_date_iso(self.time_updated)
            }