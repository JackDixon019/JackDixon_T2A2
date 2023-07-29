from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from controllers.session_count_controller import count_bp
from decorators import authorise_as_admin
from functions import delete_restricted_entity, find_all_entities, find_entity_by_id
from init import db
from models.session import Session, session_schema, sessions_schema
from models.user import User

sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")
# establishes count_bp as a child of sessions_bp
sessions_bp.register_blueprint(count_bp, url_prefix="/<int:session_id>/count")


@sessions_bp.route("/", methods=["GET"])
def get_all_sessions():
    sessions = find_all_entities(Session, Session.id)
    return sessions_schema.dump(sessions)


@sessions_bp.route("/<int:id>")
def get_one_session(id):
    session = find_entity_by_id(Session, id)
    return session_schema.dump(session)


@sessions_bp.route("/", methods=["POST"])
@jwt_required()
def create_session():
    body_data = session_schema.load(request.get_json(), partial=True)
    user = find_entity_by_id(User, get_jwt_identity())

    session = Session(
        date=body_data.get("date"),
        user_id=user.id,
        location_id=body_data.get("location_id") or user.location,
    )

    db.session.add(session)
    db.session.commit()
    return session_schema.dump(session), 201


@sessions_bp.route("/<int:id>", methods=["DELETE"])
@authorise_as_admin
def delete_session(id):
    session = find_entity_by_id(Session, id)
    return delete_restricted_entity(session, session.user_id)


# NB: no updating session counts here, they have their own endpoint
@sessions_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_session(id):
    body_data = session_schema.load(request.get_json(), partial=True)

    session = find_entity_by_id(Session, id)

    session.date = body_data.get("date") or session.date
    session.user_id = get_jwt_identity()
    session.location_id = body_data.get("location_id") or session.location_id

    db.session.commit()
    return session_schema.dump(session)
