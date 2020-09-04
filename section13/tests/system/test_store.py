from models.store import StoreModel
from models.item import ItemModel
import json

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


def test_get_all_stores_empty(test_client_db):
    res = test_client_db.get("/stores")
    assert res.status_code == 200
    assert json.loads(res.data) == {"stores": []}


def test_get_all_stores_nonempyt(test_client_db):
    s = StoreModel("test")
    s.save_to_db()
    res = test_client_db.get("/stores")
    found_store = StoreModel.find_by_name("test");
    assert res.status_code == 200
    assert json.loads(res.data) == {"stores": [found_store.json()]}


def test_get_one_existing_store(test_client_db):
    s = StoreModel("teststore")
    s.save_to_db()
    i = ItemModel("testitem", 10, 1)
    i.save_to_db()
    found_store = StoreModel.find_by_name("teststore");
    res = test_client_db.get("/store/teststore")
    assert res.status_code == 200
    assert json.loads(res.data) == found_store.json()


def test_get_one_nonexisting_store(test_client_db):
    res = test_client_db.get("/store/teststore")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Store 'teststore' not found."}


def test_post_store(test_client_db):
    res = test_client_db.post("/store/teststore")
    assert res.status_code == 201
    assert json.loads(res.data) == StoreModel.find_by_name("teststore").json()


def test_post_duplicate_store(test_client_db):
    test_client_db.post("/store/teststore")
    res = test_client_db.post("/store/teststore")
    assert res.status_code == 400
    assert json.loads(res.data) == {"message": "Store 'teststore' already exists."}


def test_delete_existing_store(test_client_db):
    test_client_db.post("/store/teststore")
    res = test_client_db.delete("/store/teststore")
    assert res.status_code == 200
    assert json.loads(res.data) == {"message": "Store 'teststore' successfully deleted."}


def test_delete_nonexisting_store(test_client_db):
    res = test_client_db.delete("/store/teststore")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Store 'teststore' not found."}



