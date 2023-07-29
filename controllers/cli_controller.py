from flask import Blueprint

from init import bcrypt, db
from models.approved_bird import ApprovedBird
from models.bird import Bird
from models.location import Location
from models.session import Session
from models.session_count import SessionCount
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
def seed_db():
    seed_all()
    print("May ye reap what ye haÞ sown...")


@db_commands.cli.command("reset")
def reset_db():
    db.drop_all()
    db.create_all()
    seed_all()
    print(
        "I have set my rainbow in the clouds, and it will be the sign of the covenant between me and the earth."
    )


def seed_all():
    # creates location objects
    locations = [
        Location(name="Sydney"),
        Location(name="Melbourne"),
        Location(name="Adelaide"),
        Location(name="Brisbane"),
    ]

    # creates user objects
    users = [
        User(
            username="user1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            location=locations[0],
        ),
        User(
            username="user2",
            email="user2@email.com",
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            location=locations[0],
        ),
        User(
            username="admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("password1").decode("utf-8"),
            is_admin=True,
            location=locations[1],
        ),
        User(
            username="admin2",
            email="admin2@email.com",
            password=bcrypt.generate_password_hash("password2").decode("utf-8"),
            is_admin=True,
            location=locations[2],
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
        Bird(
            name="Kookaburra",
            description="Rude tbh",
            submitting_user=users[2],
            is_approved=True,
        ),
        Bird(
            name="Seagull",
            description="Loud",
            submitting_user=users[1],
        ),
        Bird(
            name="Budgerigar",
            description="Chirpy, brightly coloured",
            submitting_user=users[2],
            is_approved=True,
        ),
        Bird(
            name="Snipe",
            description="Unseen?",
            submitting_user=users[0],
        ),
    ]

    approved_birds = [
        ApprovedBird(
            admin=users[2],
            bird=birds[0],
        ),
        ApprovedBird(
            admin=users[2],
            bird=birds[3],
        ),
        ApprovedBird(
            admin=users[3],
            bird=birds[5],
        ),
    ]
    # creates session objects
    sessions = [
        Session(
            user=users[0],
            session_location=locations[0],
        ),
        Session(
            user=users[0],
            session_location=locations[0],
        ),
        Session(date="2023-07-23", user=users[2], session_location=locations[1]),
        Session(date="2023-04-23", user=users[3], session_location=locations[2]),
    ]

    # creates session_count objects
    session_counts = [
        SessionCount(count=5, session=sessions[0], bird=birds[0]),
        SessionCount(count=2, session=sessions[0], bird=birds[1]),
        SessionCount(count=1, session=sessions[0], bird=birds[2]),
        SessionCount(count=5, session=sessions[1], bird=birds[0]),
        SessionCount(count=5, session=sessions[1], bird=birds[1]),
        SessionCount(count=5, session=sessions[2], bird=birds[2]),
        SessionCount(count=8, session=sessions[3], bird=birds[5]),
        SessionCount(count=20, session=sessions[3], bird=birds[4]),
        SessionCount(count=2, session=sessions[1], bird=birds[3]),
        SessionCount(count=14, session=sessions[2], bird=birds[6]),
    ]

    db.session.add_all(session_counts)
    db.session.add_all(users)
    db.session.add_all(birds)
    db.session.add_all(locations)
    db.session.add_all(sessions)
    db.session.add_all(approved_birds)
    db.session.commit()
