from controllers.cli_controller import db_commands
from controllers.bird_controller import birds_bp
from controllers.location_controller import locations_bp
from controllers.auth_controller import auth_bp
from controllers.session_controller import sessions_bp
from controllers.search_controller import search_bp

registerable_controllers = [
    db_commands,
    birds_bp,
    locations_bp,
    auth_bp,
    sessions_bp,
    search_bp,
]
