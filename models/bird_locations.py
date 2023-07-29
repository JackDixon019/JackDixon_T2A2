from init import db, ma

from datetime import datetime

# ApprovedBird allows connecting of birds with two users:
# One is the submitting user - directly connected
# The other is the approving admin - connected via ApprovedBird
class BirdLocation(db.Model):
    __tablename__ = "bird_locations"

    location_id = db.Column(db.ForeignKey("locations.id"), primary_key=True)
    bird_id = db.Column(db.ForeignKey("birds.id"), primary_key=True)
    
    location = db.relationship('User', back_populates='approved_birds')
    bird = db.relationship('Bird', back_populates='approving_location')

    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())


class ApprovedBirdSchema(ma.Schema):
    class Meta:
        fields = ("location_id", "bird_id", "date")
 

approved_bird_schema = ApprovedBirdSchema()
approved_birds_schema = ApprovedBirdSchema(many=True)