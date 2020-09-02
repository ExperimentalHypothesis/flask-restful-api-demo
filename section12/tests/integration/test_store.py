from models.store import StoreModel
from models.item import ItemModel

import pytest
from app import app
from db import db

@pytest.fixture(autouse=True)
def test_client_db():

    # set up
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    with app.app_context():
        db.init_app(app)
        db.create_all()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    # do testing
    yield testing_client

    # tear down
    with app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


def test_json(test_client_db):
    store = StoreModel("test")
    store.save_to_db()
    expected = {
            "id": 1,
            "name": "test",
            "items": [],
        }
    assert expected == store.json()

    # nonempty
    store1 = StoreModel("testing")
    store1.save_to_db()
    item1 = ItemModel("one", 10, 2)
    item2 = ItemModel("two", 10, 2)
    item1.save_to_db()
    item2.save_to_db()
    expected = {
            "id": 2,
            "name": "testing",
            "items": [
                {
                    "id": 1,
                    "name": "one",
                    "price": 10,
                    "store_id": 2,
                },
                {
                    "id": 2,
                    "name": "two",
                    "price": 10,
                    "store_id": 2,
                },
            ],
        }
    assert expected == store1.json()


def test_find_by_name(test_client_db):
    store = StoreModel("first")
    store.save_to_db()

    found = store.find_by_name("first")
    assert found.name == "first"
    assert found.id == 1
    assert list(found.items) == []

