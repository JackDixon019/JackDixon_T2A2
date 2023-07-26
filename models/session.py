from dataclasses import fields
from init import db, ma

from datetime import datetime
from marshmallow import fields


# Builds model for 'sessions' table in db
class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='user_sessions')

class SessionSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    class Meta:
        fields = ("id", "date", "user")
        ordered = True


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
