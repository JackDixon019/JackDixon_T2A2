import functools

from flask_jwt_extended import get_jwt_identity
from init import db
from models.user import User


def get_user(*args):
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    return db.session.scalar(stmt)


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_user(*args)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403
    return wrapper

def authorise_as_admin_or_original_user(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_user(*args)
        if user.is_admin or user.id == kwargs['id']:
            return fn(*args, **kwargs)
        else:
            return {"error": "Not authorised to perform action"}, 403

    return wrapper


def get_args_kwargs(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print('args = ', *args)
        print('kwargs = ', kwargs)
        return fn(*args, **kwargs)
    return wrapper


