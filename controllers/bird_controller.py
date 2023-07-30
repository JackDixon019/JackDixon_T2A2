from flask import Blueprint, request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from decorators import authorise_as_admin
from functions import delete_restricted_entity, find_entity_by_id
from init import db
from models.approved_bird import ApprovedBird
from models.bird import Bird, bird_schema
from models.user import User

birds_bp = Blueprint("birds", __name__, url_prefix="/birds")


# creates a bird
@birds_bp.route("/", methods=["POST"])
@jwt_required()
def create_bird():
    body_data = bird_schema.load(request.get_json())
    bird = Bird(
        name=body_data.get("name"),
        description=body_data.get("description"),
        submitting_user_id=get_jwt_identity(),
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
    # checks for bird in approved_birds table
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
        db.session.delete(approved_bird)
    elif user.is_admin:
        # if bird already approved, updates admin approving
        if approved_bird:
            approved_bird.admin = user
        # if bird not approved, adds bird to ApprovedBird table
        else:
            bird.is_approved = True
            approved_bird = ApprovedBird(admin=user, bird=bird)
            db.session.add(approved_bird)

    db.session.commit()
    return bird_schema.dump(bird)


@birds_bp.route("/<int:id>/approve", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def approve_bird(id):
    # gets data
    user = find_entity_by_id(User, get_jwt_identity())
    stmt = db.select(ApprovedBird).filter_by(bird_id=id)
    approved_bird = db.session.scalar(stmt)
    # checks if bird already approved
    if approved_bird:
        abort(409, f"Bird already approved by {approved_bird.admin.username}")
    # Checks bird exists
    bird = find_entity_by_id(Bird, id)
    # toggles is_approved and adds to approved_birds table
    bird.is_approved = True
    approved_bird = ApprovedBird(admin=user, bird=bird)
    db.session.add(approved_bird)
    db.session.commit()
    return bird_schema.dump(bird)
