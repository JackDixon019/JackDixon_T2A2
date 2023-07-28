from init import db, ma

class ApprovedBird(db.Model):
    __tablename__ = "approved_birds"
    admin_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    bird_id = db.Column(db.ForeignKey("birds.id"), primary_key=True)

    admin = db.relationship('User', back_populates='approved_birds')
    bird = db.relationship('Bird', back_populates='approving_admin')

class ApprovedBirdSchema(ma.Schema):
    class Meta:
        fields = ("admin_id", "bird_id")
     
approved_bird_schema = ApprovedBirdSchema()
approved_birds_schema = ApprovedBirdSchema(many=True)