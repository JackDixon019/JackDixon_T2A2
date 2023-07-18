from flask import Blueprint, request

from init import db
from models.bird import Bird, bird_schema, birds_schema


birds_bp = Blueprint("birds", __name__, url_prefix="/birds")


@birds_bp.route("/", methods=["GET"])
def get_all_birds():
    stmt = db.select(Bird).order_by(Bird.id)
    birds = db.session.scalars(stmt)
    return birds_schema.dump(birds)
 

@birds_bp.route("/<int:id>")
def get_one_bird(id):
    stmt = db.select(Bird).filter_by(id=id)
    bird = db.session.scalar(stmt)
    if bird:
        return bird_schema.dump(bird)
    return {"error": f"No bird found with id: {id}"}


@birds_bp.route("/", methods=["POST"])
def create_bird():
    body_data = bird_schema.load(request.get_json())

    bird = Bird(
        name=body_data.get("name"),
        description=body_data.get("description")
    )

    db.session.add(bird)
    db.session.commit()
    return bird_schema.dump(bird), 201


@birds_bp.route("/<int:id>", methods=["DELETE"])
def delete_bird(id):
    stmt = db.select(Bird).filter_by(id=id)
    bird = db.session.scalar(stmt)
    if bird:
        db.session.delete(bird)
        db.session.commit()
        return {"message": f"Bird '{bird.name}' deleted successfully!"}
    else:
        return {"error": f"Bird with id: {id} not found"}
    

@birds_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_bird(id):
    body_data = bird_schema.load(request.get_json(), partial=True)

    stmt = db.select(Bird).filter_by(id=id)
    bird = db.session.scalar(stmt)
    if not bird:
        return {"error": f"Bird with id: {id} not found"}
    
    bird.name=body_data.get("name") or bird.name
    bird.description=body_data.get("description") or bird.description
    bird.is_approved=False

    db.session.commit()
    return bird_schema.dump(bird)
    