from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorators import authorise_as_admin
from functions import find_entity_by_id

from init import db
from models.session import Session, session_schema, sessions_schema
from models.session_count import SessionCount, session_count_schema
from models.bird import Bird


sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")


@sessions_bp.route("/", methods=["GET"])
def get_all_sessions():
    stmt = db.select(Session).order_by(Session.id)
    sessions = db.session.scalars(stmt)
    return sessions_schema.dump(sessions)


@sessions_bp.route("/<int:id>")
def get_one_session(id):
    session = find_entity_by_id(Session, id)
    if session:
        return session_schema.dump(session)
    return {"error": f"No session found with id: {id}"}


@sessions_bp.route("/", methods=["POST"])
@jwt_required()
def create_session():
    body_data = session_schema.load(request.get_json(), partial=True)

    session = Session(
        date=body_data.get("date"), 
        user_id=get_jwt_identity(),
    )

    db.session.add(session)
    db.session.commit()
    return session_schema.dump(session), 201


@sessions_bp.route("/<int:id>/count", methods=["POST"])
@jwt_required()
def create_session_count(id):
    body_data = session_count_schema.load(request.get_json(), partial=True)

    counting_session = find_entity_by_id(Session, id)
    bird_being_counted = find_entity_by_id(Bird, body_data.get("bird_id"))

    bird_already_counted = db.session.scalar(db.select(SessionCount).filter_by(bird_id=body_data.get("bird_id"), session_id=id))
    print(bird_already_counted)
    if bird_already_counted:
        return {"Error": "This bird has already been counted this session."}
    session_count = SessionCount(
        bird=bird_being_counted,
        count=body_data.get("count"),
        session=counting_session
    )

    db.session.add(session_count)
    db.session.commit()
    return session_schema.dump(counting_session), 201


@sessions_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_session(id):
    session = find_entity_by_id(Session, id)
    if session:
        db.session.delete(session)
        db.session.commit()
        return {"message": f"session '{session.name}' deleted successfully!"}
    else:
        return {"error": f"session with id: {id} not found"}


@sessions_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_session(id):
    body_data = session_schema.load(request.get_json(), partial=True)
    
    session = find_entity_by_id(Session, id)
    if not session:
        return {"error": f"session with id: {id} not found"}

    session.date = body_data.get("date") or session.date
    session.user_id = get_jwt_identity()

    db.session.commit()
    return session_schema.dump(session)
