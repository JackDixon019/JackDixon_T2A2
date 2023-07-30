from flask import Blueprint
from flask_jwt_extended import jwt_required

from functions import find_entity_by_id, find_all_entities
from init import db
from models.bird import Bird, birds_schema, bird_schema
from models.location import Location, locations_search_schema, locations_schema, location_schema
from models.session import Session, sessions_schema, session_schema
from models.session_count import SessionCount, session_counts_schema
from models.user import User, user_schema

search_bp = Blueprint("search", __name__, url_prefix="/search")


# returns a user
@search_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = find_entity_by_id(User, id)
    return user_schema.dump(user)


# gets all birds
@search_bp.route("/birds", methods=["GET"])
def get_all_birds():
    birds = find_all_entities(Bird, Bird.id)
    return birds_schema.dump(birds)


# gets a bird
@search_bp.route("/birds/<int:id>", methods=["GET"])
def get_one_bird(id):
    bird = find_entity_by_id(Bird, id)
    return bird_schema.dump(bird)


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


@search_bp.route("/locations/", methods=["GET"])
def get_all_locations():
    stmt = db.select(Location).order_by(Location.id)
    locations = db.session.scalars(stmt)
    return locations_schema.dump(locations)


@search_bp.route("/locations/<int:id>", methods=["GET"])
def get_one_location(id):
    location = find_entity_by_id(Location, id)
    return location_schema.dump(location)


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


@search_bp.route("/sessions", methods=["GET"])
def get_all_sessions():
    sessions = find_all_entities(Session, Session.id)
    return sessions_schema.dump(sessions)


@search_bp.route("/sessions/<int:id>", methods=["GET"])
def get_one_session(id):
    session = find_entity_by_id(Session, id)
    return session_schema.dump(session)


@search_bp.route("/sessions/<int:session_id>/counts", methods=["GET"])
def get_session_counts(session_id):
    stmt = db.select(SessionCount).filter_by(session_id=session_id)
    session_counts = db.session.scalars(stmt)
    return session_counts_schema.dump(session_counts)
