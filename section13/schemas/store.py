from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.Schema):
    """ Schema for dump/load store model. """

    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        fields = ("id", "name", "items")
        include_fk = True  # tohle nevim na co tady je
