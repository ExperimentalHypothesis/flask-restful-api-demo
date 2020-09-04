from models.item import ItemModel


def test_item_init():
    item = ItemModel(name="test", price=19.99, store_id=1)
    assert item.name == "test"
    assert item.store_id == 1
    assert item.price == 19.99


def test_repr():
    item = ItemModel(name="test", price=19.99, store_id=1)
    expected = "<ItemModel test, 19.99>"
    assert expected == item.__repr__()
