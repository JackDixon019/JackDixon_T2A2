from marshmallow import fields

from init import db, ma


# Builds model for "users" table in db
# Related to Sessions, Birds, and ApprovedBirds (latter only if admin)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)

    submitted_birds = db.relationship("Bird", back_populates="submitting_user")

    approved_birds = db.relationship("ApprovedBird", back_populates="admin")

    user_sessions = db.relationship(
        "Session", back_populates="user", cascade="all, delete"
    )

    location_id = db.Column(db.Integer(), db.ForeignKey("locations.id"))
    location = db.relationship("Location", back_populates="users")


class UserSchema(ma.Schema):
    submitted_birds = fields.List(
        fields.Nested("BirdSchema", exclude=["submitting_user_id"])
    )
    user_sessions = fields.List(fields.Nested("SessionSchema", exclude=["user_id"]))
    approved_birds = fields.List(fields.Nested("ApprovedBirdSchema", only=["bird_id"]))

    class Meta:
        fields = (
            "id",
            "username",
            "password",
            "is_admin",
            "email",
            "submitted_birds",
            "user_sessions",
            "approved_birds",
        )
        ordered = True


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
