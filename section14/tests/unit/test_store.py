from models.store import StoreModel


def test_store_init():
    store = StoreModel(name="test")
    assert store.name == "test"


def test_repr():
    store = StoreModel(name="test")
    expected = "<StoreModel test>"
    assert expected == store.__repr__()
