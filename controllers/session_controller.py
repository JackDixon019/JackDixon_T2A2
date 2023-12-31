from flask import Blueprint, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import ProgrammingError

from controllers.session_count_controller import count_bp
from decorators import authorise_as_admin_or_original_user
from functions import delete_restricted_entity, find_entity_by_id
from init import db
from models.session import Session, session_schema
from models.user import User

sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")
# establishes count_bp as a child of sessions_bp
sessions_bp.register_blueprint(count_bp, url_prefix="/<int:session_id>/count")


@sessions_bp.route("/", methods=["POST"])
@jwt_required()
def create_session():
    try:
        # Get's data from body
        body_data = session_schema.load(request.get_json(), partial=True)
        # identifies user
        user = find_entity_by_id(User, get_jwt_identity())
        # creates session
        session = Session(
            date=body_data.get("date"),
            user_id=user.id,
            location_id=body_data.get("location_id") or user.location,
        )
        # adds session to database and commits
        db.session.add(session)
        db.session.commit()
        return session_schema.dump(session), 201
    except ProgrammingError as err:
        if err.orig.pgcode == errorcodes.DATATYPE_MISMATCH:
            abort(500, "Date value required for 'date' attribute")


@sessions_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_session(id):
    # finds session
    session = find_entity_by_id(Session, id)
    # deletes session if user = user who created the session or admin
    return delete_restricted_entity(session, session.user_id)


# NB: no updating session counts here, they have their own endpoint
@sessions_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_session(id):
    try:
        # finds session
        session = find_entity_by_id(Session, id)
        # this function is at the bottom of this file
        update_session_data(session, session.user_id)
        # commits changes
        db.session.commit()
        return session_schema.dump(session)
    except ProgrammingError as err:
        if err.orig.pgcode == errorcodes.DATATYPE_MISMATCH:
            abort(500, "Date value required for 'date' attribute")


# Checks user is the original user or an admin
@authorise_as_admin_or_original_user
def update_session_data(session, required_id):
    # gets body data
    body_data = session_schema.load(request.get_json(), partial=True)
    # updates details
    session.date = body_data.get("date") or session.date
    session.location_id = body_data.get("location_id") or session.location_id