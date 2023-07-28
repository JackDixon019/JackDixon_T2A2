from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from functions import delete_restricted_entity, find_all_entities, find_entity_by_id

from init import db
from models.approved_bird import ApprovedBird

from models.bird import Bird, bird_schema, birds_schema
from models.user import User
from models.session import Session
from models.location import Location

search_bp = Blueprint("search", __name__, url_prefix="/search")


models = set(Bird, User, Session, Location)

# gets all search
@search_bp.route("/", methods=["GET"])
def get_all_search():
    term = request.args.get('term')
    match term:
        case 'bird':
            find_all_entities(Bird, id)

    return birds_schema.dump(search_result)
