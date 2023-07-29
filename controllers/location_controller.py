from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from decorators import authorise_as_admin
from functions import find_entity_by_id
from init import db
from models.location import Location, location_schema, locations_schema

locations_bp = Blueprint("locations", __name__, url_prefix="/locations")


@locations_bp.route("/", methods=["GET"])
def get_all_locations():
    stmt = db.select(Location).order_by(Location.id)
    locations = db.session.scalars(stmt)
    return locations_schema.dump(locations)


@locations_bp.route("/<int:id>")
def get_one_location(id):
    location = find_entity_by_id(Location, id)
    if location:
        return location_schema.dump(location)
    return {"error": f"No location found with id: {id}"}


@locations_bp.route("/", methods=["POST"])
def create_location():
    body_data = location_schema.load(request.get_json())

    location = location(
        name=body_data.get("name"), description=body_data.get("description")
    )

    db.session.add(location)
    db.session.commit()
    return location_schema.dump(location), 201


@locations_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_location(id):
    location = find_entity_by_id(Location, id)
    if location:
        db.session.delete(location)
        db.session.commit()
        return {"message": f"location '{location.name}' deleted successfully!"}
    else:
        return {"error": f"location with id: {id} not found"}


@locations_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@authorise_as_admin
def update_location(id):
    body_data = location_schema.load(request.get_json(), partial=True)

    location = find_entity_by_id(Location, id)

    location.name = body_data.get("name") or location.name

    db.session.commit()
    return location_schema.dump(location)
