from controllers.cli_controller import db_commands
from controllers.bird_controller import birds_bp
from controllers.location_controller import locations_bp
from controllers.auth_controller import auth_bp

registerable_controllers = [
    db_commands,
    birds_bp,
    locations_bp,
    auth_bp,
]
