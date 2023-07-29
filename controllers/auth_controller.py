from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError

from functions import delete_restricted_entity, find_entity_by_id
from init import bcrypt, db
from models.user import User, user_schema

# defines blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# allows user registration
@auth_bp.route("/register", methods=["POST"])
def create_user():
    try:
        # gets data from request body, adds it to user object
        body_data = request.get_json()
        user = User()
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(
                body_data.get("password")
            ).decode("utf-8")
        user.username = body_data.get("username")
        user.email = body_data.get("email")

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"Required field: {err.orig.diag.column_name} empty"}, 409


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
        return {"error": "Incorrect username or password"}


# deletes existing user
@auth_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
# allows only either an admin or the user themselves to delete
def delete_user(id):
    user = find_entity_by_id(User, id)
    print("flag")
    # deletes only unapproved_birds
    for bird in user.submitted_birds:
        if bird.is_approved == False:
            db.session.delete(bird)
    return delete_restricted_entity(user, user.id)


# returns a user
@auth_bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = find_entity_by_id(User, id)
    if user:
        return user_schema.dump(user)
