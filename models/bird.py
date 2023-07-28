from init import db, ma

from marshmallow import fields, post_dump

# Builds model for 'birds' table in db
class Bird(db.Model):
    __tablename__ = "birds"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    
    is_approved = db.Column(db.Boolean(), default=False)

    approving_admin = db.relationship('ApprovedBird', back_populates='bird', uselist=False)

    submitting_user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    submitting_user = db.relationship('User', back_populates='submitted_birds')

    session_counts = db.relationship('SessionCount', back_populates='bird', cascade='all, delete')


class BirdSchema(ma.Schema):
    
    approving_admin = fields.Nested("ApprovedBirdSchema", only=['admin_id'])

    @post_dump
    def remove_approving_admin(self, data, **kwargs):
        if data["is_approved"] == True:
            return {
                key:value for key, value in data.items()
            }
        else:
            return {
                key:value for key, value in data.items()
                if key != "approving_admin"
            }
    class Meta:
        fields = ("id", "name", "description", "is_approved", "submitting_user_id", "approving_admin")
        ordered = True


bird_schema = BirdSchema()
birds_schema = BirdSchema(many=True)