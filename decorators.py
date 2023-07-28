import functools

from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from init import db
from models.user import User



# just gets user id
def get_user():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    if db.session.scalar(stmt):
        return db.session.scalar(stmt)
    else:
        raise ValidationError(f'Current user no longer exists')


# Passes through function if user is an admin, otherwise throws error
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_user()
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403
    return wrapper


# checks that user is admin or original user, throws error otherwise
def authorise_as_admin_or_original_user(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_user()
        required_id = args[1]
        print(user.id)
        # print(user.is_admin)
        print(required_id)
        if user.is_admin or user.id == required_id:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403
    return wrapper