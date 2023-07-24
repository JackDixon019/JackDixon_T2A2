from init import db, ma

from datetime import datetime


# Builds model for 'sessions' table in db
class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, default=datetime.today().date())
    user_id = db.Column(db.Integer(), nullable=False)

class SessionSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "user_id")
        ordered = True


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
