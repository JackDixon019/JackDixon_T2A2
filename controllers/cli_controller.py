from flask import Blueprint

from init import db

from models.bird import Bird

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
        description="Choncc"
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

    db.session.add_all(birds)
    db.session.commit()
    print("May ye reap what ye haÞ sown...")