from marshmallow import fields, post_dump
from sqlalchemy import null

from init import db, ma


# Builds model for "birds" table in db
class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)
    # relates birds and users
    submitting_user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    submitting_user = db.relationship("User", back_populates="submitted_birds")
    # relation with admin via ApprovedBird join table.
    # While I don"t think a join table is strictly necessary for a 1-to-many relationship,
    # I couldn"t make two connections directly from Bird to User without issues
    approving_admin = db.relationship(
        "ApprovedBird", back_populates="bird", uselist=False, cascade="all, delete"
    )
    # relates birds with session_counts
    session_counts = db.relationship(
        "SessionCount", back_populates="bird", cascade="all, delete"
    )


class BirdSchema(ma.Schema):
    # Normally I"d use an admin_id field, but it caused circular dependencies
    approving_admin = fields.Nested("ApprovedBirdSchema", only=["admin_id"])

    @post_dump
    def remove_null_fields(self, data, **kwargs):
        # This skips null value fields
        result = {key: value for key, value in data.items() if value != None}
        # If original user was deleted, returns "user_deleted" as a result
        if "submitting_user_id" not in result:
            result["submitting_user_id"] = "User Deleted"
        return result

    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "is_approved",
            "approving_admin",
            "submitting_user_id",
        )
        ordered = True


bird_schema = BirdSchema()
birds_schema = BirdSchema(many=True)
