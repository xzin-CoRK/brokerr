from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy import event, text
from sqlalchemy.orm import relationship
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(256), unique=True)
    salt = Column(String(100))
    last_login = Column(DateTime)

class Tracker(db.Model):
    __tablename__ = "tracker"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    login_url = Column(Text)
    last_captured = Column(DateTime)
    times_captured = Column(Integer)
    favicon_path = Column(String(256))
    salt = Column(String(100))
    credentials = Column(Text)

class Insurance(db.Model):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer,
                            ForeignKey('tracker.id'),
                            nullable=False)
    tracker = relationship('Tracker', backref='insurances')
    insurance_date = Column(DateTime)
    image_path = Column(String(256))


@event.listens_for(Insurance, 'after_insert')
def after_insert_insurance(mapper, connection, target):
    """
    Event listener that fires after a new screenshot capture is logged in the Insurance table.
    Will update the tracker's last_captured field and increment times_captured
    """
    trigger_sql = '''
                UPDATE tracker
                SET times_captured = COALESCE(times_captured, 0) + 1,
                    last_captured = :insurance_date
                WHERE id = :tracker_id;
    '''

    connection.execute(
        text(trigger_sql),
        tracker_id = target.tracker_id,
        insurance_date = target.insurance_date
    )