from models.item import ItemModel
from models.store import StoreModel


def test_store_init():
    item = ItemModel("test", 19.99, 1)
    assert item.name == "test"
    assert item.store_id == 1
    assert item.price == 19.99

def test_repr():
    item = ItemModel("test", 19.99, 1)
    expected = "<Itemmodel test, 19.99>"
    assert expected == item.__repr__()

# def test_json():
#     item = ItemModel("test", 19.99, 1)
#     expected = {"id": None,  # tadyto uz je interakce s databazi a ma to jit to integration testu..
#                 "name": "test",
#                 "price": 19.99,
#                 "store_id": 1
#     }
#     assert expected == item.json()


