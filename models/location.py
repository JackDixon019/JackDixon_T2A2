from init import db, ma

from marshmallow import fields

# Builds model for 'locations' table in db
class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    sessions = db.relationship('Session', back_populates='session_location', cascade="all, delete")

    users = db.relationship('User', back_populates='location')


class LocationSchema(ma.Schema):
    sessions = fields.List(fields.Nested('SessionSchema', only=['id', "user_id"]))
    users = fields.List(fields.Nested('UserSchema', only=['id']))
    class Meta:
        fields = ("id", "name", "sessions")
        ordered = True


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
