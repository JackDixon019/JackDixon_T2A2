from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from functions import delete_restricted_entity, find_all_entities, find_entity_by_id
from sqlalchemy.orm import selectin_polymorphic

from init import db
from models.approved_bird import ApprovedBird
from models.bird import Bird, bird_schema, birds_schema
from models.session_count import SessionCount, session_counts_schema
from models.user import User
from models.session import Session, sessions_schema


birds_bp = Blueprint("birds", __name__, url_prefix="/birds")


# gets all birds
@birds_bp.route("/", methods=["GET"])
def get_all_birds():
    birds = find_all_entities(Bird, Bird.id)
    return birds_schema.dump(birds)


# filters all_birds b y user
@birds_bp.route("/user/<int:user_id>", methods=["GET"])
def get_birds_by_user(user_id):
    stmt = db.select(Bird).filter_by(submitting_user_id=user_id)
    birds = db.session.scalars(stmt)
    return birds_schema.dump(birds)

# filter_by(location_id=location_id)
# filters all_birds b y location
@birds_bp.route("/location/<int:location_id>", methods=["GET"])
def get_birds_by_location(location_id):
    birds = set()
    options = selectin_polymorphic(Session, [SessionCount])
    stmt = db.select(Session).filter_by(location_id=location_id).options(options)
    sessions = db.session.scalars(stmt).all()
    for i in range(len(sessions)):
        sesh_counts = sessions[i].session_counts
        for j in sesh_counts:
            birds.add(j.bird_id)
    return {f"birds at location: {location_id}": f'{birds}'}


# gets a bird
@birds_bp.route("/<int:id>", methods=["GET"])
def get_one_bird(id):
    bird = find_entity_by_id(Bird, id)
    return bird_schema.dump(bird)


# creates a bird
@birds_bp.route("/", methods=["POST"])
@jwt_required()
def create_bird():
    body_data = bird_schema.load(request.get_json())

    bird = Bird(
        name=body_data.get("name"), 
        description=body_data.get("description"),
        submitting_user_id=get_jwt_identity()
        )

    db.session.add(bird)
    db.session.commit()
    return bird_schema.dump(bird), 201


# deletes a bird
@birds_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_bird(id):
    bird = find_entity_by_id(Bird, id)
    return delete_restricted_entity(bird, bird.submitting_user_id)


# updates a bird
@birds_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_bird(id):
    # gets data
    body_data = bird_schema.load(request.get_json(), partial=True)
    user = find_entity_by_id(User, get_jwt_identity()) 

    stmt = db.select(ApprovedBird).filter_by(bird_id=id)
    approved_bird = db.session.scalar(stmt)
    # finds bird in table
    bird = find_entity_by_id(Bird, id)
    #  updates details
    bird.name = body_data.get("name") or bird.name
    bird.description = body_data.get("description") or bird.description
    bird.submitting_user_id = user.id
    # if user is not admin, unapproves bird
    if approved_bird and not user.is_admin:
        bird.is_approved = False
        # removes bird from ApprovedBird table
        if approved_bird:
            db.session.delete(approved_bird)
    elif user.is_admin:
        # if bird already approved, updates admin approving
        if approved_bird:
            approved_bird.admin_id = user.id
        # if bird not approved, adds bird to ApprovedBird table
        else:
            bird.is_approved = True
            approved_bird = ApprovedBird(
                admin=user,
                bird=bird
            )
            db.session.add(approved_bird)

    db.session.commit()
    return bird_schema.dump(bird)
