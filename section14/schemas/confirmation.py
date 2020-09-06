from ma import ma
from models.confirmation import ConfirmationModel
from models.user import UserModel


class ConfirmationSchema(ma.Schema):
    """ Schema for dump/load confirmation model. """

    class Meta:
        model = ConfirmationModel
        fields = ("id", "user_id", "expire_at", "confirmed")
        load_only = ("user", )
        dump_only = ("id", "expired_at", "confirmed")
        include_fk = True

