from models.item import ItemModel
from models.store import StoreModel

import pytest
from app import app
from db import db


@pytest.fixture(scope="module")
def test_client_db():

    # set up
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    with app.app_context():
        db.init_app(app)
        db.create_all()

    testing_client = app.test_client() 
    ctx = app.app_context()
    ctx.push()
    yield testing_client

    # tear down
    with app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


def test_json(test_client_db):
    item = ItemModel("test", 19.99, 1)
    item.save_to_db()
    expected = {"id": 1,  # tadyto uz je interakce s databazi a ma to jit to integration testu..
                "name": "test",
                "price": 19.99,
                "store_id": 1
    }
    assert expected == item.json()
