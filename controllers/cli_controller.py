from flask import Blueprint

from init import db

from models.bird import Bird
from models.location import Location

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_all():
    db.create_all()
    print("Let there be Tables!")


@db_commands.cli.command("yeet")
def drop_all():
    db.drop_all()
    print("And then there was nothing...")


@db_commands.cli.command("seed")
def seed_all():
    # Creates Bird objects
    birds = [
        Bird(
        name="Pigeon",
        description="Choncc",
        is_approved=True
        ),

        Bird(
        name="Cockatoo",
        description="Loud"
        ),

        Bird(
        name="Lorikeet",
        description="Gay"
        )
    ]

    locations = [
        Location(
        name="Sydney"
        ),

        Location(
        name="Melbourne"
        ),

        Location(
        name="Adelaide"
        ),
        
        Location(
        name="Brisbane"
        )
    ]

    db.session.add_all(birds)
    db.session.add_all(locations)
    db.session.commit()
    print("May ye reap what ye haÞ sown...")