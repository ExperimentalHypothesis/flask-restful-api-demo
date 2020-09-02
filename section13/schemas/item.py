from ma import ma
from models.item import ItemModel
from models.store import StoreModel  # import for fk


class ItemSchema(ma.Schema):
    """ Schema for dump/load item model. """

    class Meta:
        model = ItemModel
        fields = ("id", "name",)
