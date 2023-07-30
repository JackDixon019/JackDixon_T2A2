from datetime import timedelta

from flask import Blueprint, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

from functions import delete_restricted_entity, find_entity_by_id
from init import bcrypt, db
from models.user import User, user_schema, user_register_schema
from models.location import Location

# defines blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# allows user registration
@auth_bp.route("/register", methods=["POST"])
def create_user():
    try:
        # gets data from request body
        # user_register_schema is used to validate data -> password is excluded from user_schema which caused errors
        body_data = user_register_schema.load(request.get_json())
        user = User()
        password = body_data.get("password")
        if password:
            # encrypts password
            user.password = bcrypt.generate_password_hash(
                body_data.get("password")
            ).decode("utf-8")
        user.username = body_data.get("username")
        user.email = body_data.get("email")
        user.location_id = body_data.get("location_id")
        # adds user to db
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            abort(409, "Email address already in use")
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            abort(400, f"Required field: {err.orig.diag.column_name} empty")


# allows users to login, returns an auth token
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # checks hashed password aligns with submitted one
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=7)
        )
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    else:
        abort(401, "Incorrect username or password")


# deletes existing user
@auth_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = find_entity_by_id(User, id)
    # deletes only unapproved_birds
    for bird in user.submitted_birds:
        if bird.is_approved == False:
            db.session.delete(bird)
    # allows only either an admin or the user themselves to delete
    # The session isn't committed until this step, so if the user auth fails the bird doesn't remain deleted
    return delete_restricted_entity(user, user.id)


# Allows user to update their location
@auth_bp.route("/location/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_location(id):
    user = find_entity_by_id(User, get_jwt_identity())
    location = find_entity_by_id(Location, id)
    user.location = location
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user)
    
