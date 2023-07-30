from flask import Blueprint
from flask_jwt_extended import jwt_required

from functions import find_entity_by_id
from init import db
from models.bird import Bird, birds_schema
from models.location import Location, locations_search_schema
from models.session import Session
from models.session_count import SessionCount
from models.user import User

search_bp = Blueprint("search", __name__, url_prefix="/search")


# filters all_birds by user
@search_bp.route("/birds_by_user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_birds_by_user(user_id):
    # checks user exists
    find_entity_by_id(User, user_id)
    # filters birds and returns json
    stmt = db.select(Bird).filter_by(submitting_user_id=user_id)
    birds = db.session.scalars(stmt)
    return birds_schema.dump(birds)


# filters all_birds by location
@search_bp.route("/birds_by_location/<int:location_id>", methods=["GET"])
def get_birds_by_location(location_id):
    # checks location exists
    find_entity_by_id(Location, location_id)
    # I probably should've just made a join table but I thought this would be easier... Lesson learned
    stmt = (
        db.select(Bird)
        # This joins the other tables all together to connect birds and locations
        .join(Bird.session_counts)
        .join(SessionCount.session)
        .join(Session.session_location.and_(Location.id == location_id))
        # prevents duplicates
        .distinct()
    )
    birds = db.session.scalars(stmt)
    return birds_schema.dump(birds)


# filters locations by bird
@search_bp.route("/locations_by_bird/<int:bird_id>", methods=["GET"])
def get_locations_by_bird(bird_id):
    # checks bird exists
    find_entity_by_id(Bird, bird_id)
    stmt = (
        db.select(Location)
        # This joins the other tables all together to connect locations and birds
        .join(Location.sessions)
        .join(Session.session_counts)
        .join(SessionCount.bird.and_(Bird.id == bird_id))
        # prevents duplicates
        .distinct()
    )
    locations = db.session.scalars(stmt)
    return locations_search_schema.dump(locations)