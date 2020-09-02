from ma import ma
from models.item import ItemModel
from models.store import StoreModel  # import for fk


class ItemSchema(ma.Schema):
    """ Schema for dump/load item model. """

    class Meta:
        model = ItemModel
        fields = ("id", "name", "price", "store_id") # timhle rikam jaky atributy budu posilat na odpoved
        # dump_only = ("id")  # tohle neposilam, to prida sqlalchemy
        # load_only = ("name",)
        include_fk = True
