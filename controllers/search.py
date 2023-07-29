from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from functions import delete_restricted_entity, find_all_entities, find_entity_by_id
from sqlalchemy import MetaData

from init import db
from models.approved_bird import ApprovedBird

from models.bird import Bird, bird_schema, birds_schema
from models.user import User
from models.session import Session
from models.location import Location

search_bp = Blueprint("search", __name__, url_prefix="/search")




# gets all search
@search_bp.route("/", methods=["GET"])
# @jwt_required()
def get_all_search():
    body_data = request.get_json()
    term1 = body_data.get("term1")
    term2 = body_data.get("term2")
    term3 = body_data.get("term3")
    id1 = body_data.get("id1")
    id2 = body_data.get("id2")
