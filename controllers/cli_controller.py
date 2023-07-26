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
    
    # Creates Bird objects
    birds = [
        Bird(
            name="Pigeon",
            description="Choncc",
            submitting_user=users[2],
            is_approved=True,
        ),
        Bird(
            name="Cockatoo",
            description="Loud",
            submitting_user=users[0],
            ),
        Bird(
            name="Lorikeet",
            description="Gay",
            submitting_user=users[1],
            ),
    ]

    locations = [
        Location(name="Sydney"),
        Location(name="Melbourne"),
        Location(name="Adelaide"),
        Location(name="Brisbane"),
    ]

    sessions = [
        Session(
            user=users[0]
        ),
        Session(
            user=users[0]
        ),
        Session(
        date="2023-07-23",
        user=users[2]
        )
    ]


    db.session.add_all(users)
    db.session.add_all(birds)
    db.session.add_all(locations)
    db.session.add_all(sessions)
    db.session.commit()
    print("May ye reap what ye haÞ sown...")
