from init import db, ma


# Builds model for 'birds' table in db
class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        ordered = True


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
