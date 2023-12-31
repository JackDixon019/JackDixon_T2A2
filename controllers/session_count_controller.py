from flask import Blueprint, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from functions import find_entity_by_id
from init import db
from models.bird import Bird
from models.session import Session, session_schema
from models.session_count import SessionCount, session_count_schema
from models.user import User

count_bp = Blueprint("session_counts", __name__)


@count_bp.route("/", methods=["POST"])
@jwt_required()
def create_session_count(session_id):
    # gets data from request body
    body_data = session_count_schema.load(request.get_json(), partial=True)
    user_id = get_jwt_identity()

    # finds the session and the bird from body data
    # find_entity_by_id handles error in case entity doesn't exist
    counting_session = find_entity_by_id(Session, session_id)
    bird_being_counted = find_entity_by_id(Bird, body_data.get("bird_id"))

    # checks user is correct user to add a session count
    if user_id != counting_session.user_id:
        abort(403, "Not authorised to perform action")
    # Checks whether this bird has already been counted in this session
    stmt = db.select(SessionCount).filter_by(
        bird_id=body_data.get("bird_id"), session_id=session_id
    )
    bird_already_counted = db.session.scalar(stmt)
    if bird_already_counted:
        abort(409, "This bird has already been counted this session.")
    # Creates session_count object
    session_count = SessionCount(
        bird=bird_being_counted, count=body_data.get("count"), session=counting_session
    )
    # adds session_count to db
    db.session.add(session_count)
    db.session.commit()
    return session_schema.dump(counting_session), 201


@count_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_session_count(session_id, id):
    # checks whether session_count being edited is associated with the session
    session_count = find_entity_by_id(SessionCount, id)
    if session_count.session_id != session_id:
        return {
            "Error": f"The session with id: {session_id} is not associated with the count you wish to edit."
        }

    # finds session and user entities by id
    counting_session = find_entity_by_id(Session, session_id)
    user = find_entity_by_id(User, get_jwt_identity())

    # only allows original user or admin to edit data
    if user.is_admin == False and counting_session.user_id != user.id:
        abort(403, "Not authorised to perform action")
    # gets body data from request
    body_data = session_count_schema.load(request.get_json(), partial=True)
    bird_id = body_data.get("bird_id")

    if bird_id:
        # fetches bird entity, also checks if it exists
        bird_being_counted = find_entity_by_id(Bird, bird_id)
        # updates entry with the new data
        session_count.bird = bird_being_counted

        # counts session_counts with the same bird, rejects update if more than 1 exists
        stmt = (
            db.select(db.func.count())
            .select_from(SessionCount)
            .filter_by(bird_id=bird_id, session_id=session_id)
        )
        bird_count = db.session.scalar(stmt)

        # "> 1" is the number to check, since the data has already been updated so there must be at least 1
        if bird_count > 1:
            abort(409, "This bird has already been counted this session.")
    # updates entry with new count if it exists
    session_count.count = body_data.get("count") or session_count.count
    # adds and commits new data
    db.session.add(session_count)
    db.session.commit()
    return session_schema.dump(counting_session), 201
