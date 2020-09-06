from ma import ma
from marshmallow import pre_dump
from models.user import UserModel


class UserSchema(ma.Schema):
    """ Schema for dump/load user model. """

    class Meta:
        model = UserModel  # flask-marmallow will no create object directly based on the database schema
        fields = ("username", "password", "id", "email")
        load_only = ("password",)  # tohle jenom prijimat ale nikdy neposilat ven jako dzejson
        dump_only = ("id", "activated")  # tohle neni potreba davat to prida sqlalch

        @pre_dump
        def _pre_dump(self, user: UserModel):
            user.confirmation = [user.get_latest_confirmation]
            return user
