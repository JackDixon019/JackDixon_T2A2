from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from functions import delete_admin_entity, find_all_entities, find_entity_by_id

from init import db
from models.approved_bird import ApprovedBird
from models.bird import Bird, bird_schema, birds_schema
from models.user import User


birds_bp = Blueprint("birds", __name__, url_prefix="/birds")


@birds_bp.route("/", methods=["GET"])
def get_all_birds():
    birds = find_all_entities(Bird, Bird.id)
    return birds_schema.dump(birds)


@birds_bp.route("/<int:id>", methods=["GET"])
def get_one_bird(id):
    bird = find_entity_by_id(Bird, id)
    if bird:
        return bird_schema.dump(bird)
    return {"error": f"No bird found with id: {id}"}


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


@birds_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_bird(id):
    bird = find_entity_by_id(Bird, id)
    if bird:
        # Only admins allowed to delete approved birds
        if bird.is_approved == True:
            return delete_admin_entity(bird)
        # Only allows original user or admin to delete birds
        user = find_entity_by_id(User, get_jwt_identity())
        if user.id != bird.submitting_user_id and not user.is_admin:
            return {"error": "Not authorised to perform action. Only original user may delete."}, 403
        
        db.session.delete(bird)
        db.session.commit()
        return {"message":f"Bird with id: {id} successfully deleted"}
    else:
        return {"error": f"Bird with id: {id} not found"}


@birds_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_bird(id):
    # gets body data
    body_data = bird_schema.load(request.get_json(), partial=True)
    # finds bird in table
    bird = find_entity_by_id(Bird, id)
    #  updates details, toggles is_approved
    bird.name = body_data.get("name") or bird.name
    bird.description = body_data.get("description") or bird.description
    bird.submitting_user_id = get_jwt_identity()
    bird.is_approved = False

    # removes bird from ApprovedBird table
    stmt = db.select(ApprovedBird).filter_by(bird_id=id)
    approved_bird = db.session.scalar(stmt)
    if approved_bird:
        db.session.delete(approved_bird)

    db.session.commit()
    return bird_schema.dump(bird)
