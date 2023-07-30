import os

from flask import Flask
from marshmallow import ValidationError

from controllers.__init__ import registerable_controllers
from init import bcrypt, db, jwt, ma


def create_app():
    app = Flask(__name__)

    # Stop json keys from sorting
    app.json.sort_keys = False

    # Get variables from .env file
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def return_error(err):
        return {"error": str(err)}, 400

    @app.errorhandler(400)
    def return_error(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(401)
    def return_error(err):
        return {"error": str(err)}, 401
    
    @app.errorhandler(403)
    def return_error(err):
        return {"error": str(err)}, 403

    @app.errorhandler(404)
    def return_error(err):
        return {"error": str(err)}, 404

    @app.errorhandler(409)
    def return_error(err):
        return {"error": str(err)}, 409
    
    @app.errorhandler(410)
    def return_error(err):
        return {"error": str(err)}, 410
    
    @app.errorhandler(500)
    def return_error(err):
        return {"error": str(err)}, 500

    # Calls objects within function to prevent double-import errors
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
