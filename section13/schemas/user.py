from ma import ma
from models.user import UserModel


class UserSchema(ma.Schema):
    """ Schema for dump/load user model. """

    class Meta:
        model = UserModel  # flask-marmallow will no create object directly based on the database schema
        fields = ("username", "password")
        load_only = ("password",)
        dump_only = ("id",)
