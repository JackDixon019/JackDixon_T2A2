from init import db, ma

from marshmallow import fields, validate


# Builds model for 'sessions' table in db
class SessionCount(db.Model):
    __tablename__ = 'session_counts'

    id = db.Column(db.Integer(), primary_key=True)
    count = db.Column(db.Integer(), nullable=False)

    session_id = db.Column(db.Integer(), db.ForeignKey('sessions.id'), nullable=False)
    session = db.relationship('Session', back_populates='session_counts')

    bird_id = db.Column(db.Integer(), db.ForeignKey('birds.id'), nullable=False)
    bird = db.relationship('Bird', back_populates='session_counts')


class SessionCountSchema(ma.Schema):
    count = validate.Range(min=0)
    bird = fields.Nested('BirdSchema', only=['id'])
    class Meta:
        fields = ('id', 'session_id', 'bird_id', 'bird', 'count')
        ordered = True

session_count_schema = SessionCountSchema()
session_counts_schema = SessionCountSchema(many=True)
