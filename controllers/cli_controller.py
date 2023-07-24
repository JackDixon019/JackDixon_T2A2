from flask import Blueprint

from init import db, bcrypt

from models.bird import Bird
from models.location import Location
from models.session import Session
from models.user import User

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
        Bird(name="Pigeon", description="Choncc", is_approved=True),
        Bird(name="Cockatoo", description="Loud"),
        Bird(name="Lorikeet", description="Gay"),
    ]

    locations = [
        Location(name="Sydney"),
        Location(name="Melbourne"),
        Location(name="Adelaide"),
        Location(name="Brisbane"),
    ]

    users = [
        User(
            username="user1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
        ),
        User(
            username="user2",
            email="user2@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
        ),
        User(
            username="admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("password1").decode("utf-8"),
            is_admin=True,
        ),
    ]


    sessions = [
        Session(
            user_id=1
        ),
        Session(
            user_id=2
        ),
        Session(
        date="2023-07-23",
        user_id=1
        )
    ]


    db.session.add_all(users)
    db.session.add_all(birds)
    db.session.add_all(locations)
    db.session.add_all(sessions)
    db.session.commit()
    print("May ye reap what ye haÞ sown...")
