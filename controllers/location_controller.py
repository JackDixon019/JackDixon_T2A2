from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

from decorators import authorise_as_admin
from functions import delete_admin_entity, find_entity_by_id
from init import db
from models.location import Location, location_schema, location_search_schema

locations_bp = Blueprint("locations", __name__, url_prefix="/locations")


@locations_bp.route("/", methods=["POST"])
@jwt_required()
def create_location():
    try:
        body_data = location_schema.load(request.get_json())
        location = Location(name=body_data.get("name"))
        db.session.add(location)
        db.session.commit()
        return location_search_schema.dump(location), 201
    # Catches if name field is left empty
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            abort(400, f"Required field: {err.orig.diag.column_name} empty")


@locations_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_location(id):
    location = find_entity_by_id(Location, id)
    # delete_admin_entity checks for admin rights
    return delete_admin_entity(location)


@locations_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_location(id):
    body_data = location_schema.load(request.get_json(), partial=True)
    location = find_entity_by_id(Location, id)
    location.name = body_data.get("name") or location.name
    db.session.commit()
    return location_schema.dump(location)
