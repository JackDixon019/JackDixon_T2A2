from controllers.cli_controller import db_commands
from controllers.bird_controller import birds_bp

registerable_controllers = [
    db_commands,
    birds_bp
]