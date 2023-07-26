from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from functions import find_entity_by_id

from init import db
from models.bird import Bird, bird_schema, birds_schema


birds_bp = Blueprint("birds", __name__, url_prefix="/birds")


@birds_bp.route("/", methods=["GET"])
def get_all_birds():
    stmt = db.select(Bird).order_by(Bird.id)
    birds = db.session.scalars(stmt)
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
def delete_bird(id):
    bird = find_entity_by_id(Bird, id)
    if bird:
        db.session.delete(bird)
        db.session.commit()
        return {"message": f"Bird '{bird.name}' deleted successfully!"}
    else:
        return {"error": f"Bird with id: {id} not found"}


@birds_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_bird(id):
    body_data = bird_schema.load(request.get_json(), partial=True)

    bird = find_entity_by_id(Bird, id)
    if not bird:
        return {"error": f"Bird with id: {id} not found"}

    bird.name = body_data.get("name") or bird.name
    bird.description = body_data.get("description") or bird.description
    bird.submitting_user_id = get_jwt_identity()
    bird.is_approved = False

    db.session.commit()
    return bird_schema.dump(bird)
