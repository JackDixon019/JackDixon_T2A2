from init import db, ma

from marshmallow import fields

# Builds model for 'birds' table in db
class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)

    submitting_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    submitting_user = db.relationship('User', back_populates='submitted_birds')

     

class BirdSchema(ma.Schema):
    submitting_user = fields.Nested('UserSchema', only=['username'])
    class Meta:
        fields = ("id", "name", "description", "is_approved", "submitting_user")
        ordered = True


bird_schema = BirdSchema()
birds_schema = BirdSchema(many=True)
