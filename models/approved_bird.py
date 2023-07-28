from init import db, ma

from datetime import datetime
from marshmallow import validate, validates

# ApprovedBird allows connecting of birds with two users:
# One is the submitting user - directly connected
# The other is the approving admin - connected via ApprovedBird
class ApprovedBird(db.Model):
    __tablename__ = "approved_birds"

    admin_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    bird_id = db.Column(db.ForeignKey("birds.id"), primary_key=True)
    
    admin = db.relationship('User', back_populates='approved_birds')
    bird = db.relationship('Bird', back_populates='approving_admin')

    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())


class ApprovedBirdSchema(ma.Schema):
    class Meta:
        fields = ("admin_id", "bird_id", "date")
 

approved_bird_schema = ApprovedBirdSchema()
approved_birds_schema = ApprovedBirdSchema(many=True)