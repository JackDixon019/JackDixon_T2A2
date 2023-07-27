import os

from flask import Flask
from marshmallow import ValidationError

from init import bcrypt, db, jwt, ma
from controllers.__init__ import registerable_controllers


def create_app():
    app = Flask(__name__)

    # Stop json keys from sorting
    app.json.sort_keys = False

    # Get variables from .env file
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error':str(err)}, 400
    
    @app.errorhandler(400)
    def validation_error(err):
        return {'error':str(err)}, 400
    
    @app.errorhandler(404)
    def validation_error(err):
        return {'error':str(err)}, 404

    # Calls objects within function to prevent double-import errors
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
