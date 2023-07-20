from init import db, ma


# Builds model for 'users' table in db
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "is_admin", "email")
        ordered = True


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
