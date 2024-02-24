from redis import Redis
from sqlalchemy import select
from config.settings import REDIS_URL

from app.extensions import db
from data.model import Insurance, Tracker, User

redis_db = Redis.from_url(REDIS_URL)

def get_user_by_id(user_id: str):
    return db.session.scalars(
        select(User).where(User.id==int(user_id))
    ).one_or_none()

def get_recent_insurance(tracker: str) -> list:
    results = db.session.execute(db.select(Insurance).filter_by(tracker_id=tracker)).scalars()
    return results

def get_trackers() -> list:
    return Tracker.query.all()

def get_tracker_stats(tracker_id: int) -> any:
    return Insurance.query.filter_by(tracker_id=tracker_id).scalar_one()

def store_success(tracker_id, timestamp, image_path):
    insurance = Insurance()
    insurance.tracker_id = tracker_id
    insurance.image_path = image_path
    insurance.insurance_date = timestamp

    db.session.add(insurance)
    db.session.commit()

def get_user_by_username(username: str) -> (User | None):
    """
    Return a User based on their username
    
    :param username: The user to retrieve
    :return: User object if found, otherwise None
    """
    return db.session.scalars(
        select(User).where(User.username==username)
    ).one_or_none()


def get_trackers_without_favicon():
    return Tracker.query.filter(Tracker.favicon_path.is_(None)).all()
        
def is_master_pass_set() -> bool:
    if not redis_db.exists('master_password'):
        return False
    elif redis_db.get('master_password') is None:
        return False
    else:
        return True

def try_set_master_pass(old_password: str, new_password: str) -> dict:
    existing_pass = redis_db.get('master_password')

    if existing_pass is None:
        if redis_db.set('master_password', new_password):
            return {
                "success": True,
                "message": "Password set"
            }

    if old_password != existing_pass:
        return {
            "success": False,
            "message": "Password doesn't match"
        }
        
    if existing_pass == old_password:
        if redis_db.set('master_password', new_password):
            return {
                "success": True,
                "message": "Password updated successfully"
            }
    
    # Something went wrong
    return {
        "success": False,
        "message": "An error occurred. Please try again."
    }