from init import db, ma

# Builds model for 'birds' table in db
class Bird(db.Model):
    __tablename__ = 'birds'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)


class BirdSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'is_approved')
        ordered = True

bird_schema = BirdSchema()
birds_schema = BirdSchema(many=True)

