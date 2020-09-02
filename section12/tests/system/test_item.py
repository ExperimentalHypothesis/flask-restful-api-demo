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


def test_get_all_items_empty(test_client_db):
    res = test_client_db.get("/items")
    assert res.status_code == 200
    assert json.loads(res.data) == {"items": []}


def test_get_all_items_non_empty(test_client_db):
    i = ItemModel("test", 10, 1)
    i.save_to_db()
    res = test_client_db.get("/items")
    assert res.status_code == 200
    assert json.loads(res.data) == {"items": [i.json()]}  # i have already tested json method so i can use it here


def test_get_single_existing_item(test_client_db):
    i = ItemModel("test", 10, 1)
    i.save_to_db()
    res = test_client_db.get("/item/test")
    assert res.status_code == 200
    assert json.loads(res.data) == i.json()


def test_get_single_nonexisting_item(test_client_db):
    res = test_client_db.get("/item/test")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Item 'test' not found."}


def test_post_item(test_client_db):
    res = test_client_db.post("/item/test", data={"price": 12, "store_id": 1})
    assert res.status_code == 201  # bach na JTW REQUIRED.. musim pak dopsat
    item = ItemModel.find_item_by_name("test")
    assert json.loads(res.data) == item.json()


def test_post_duplicate_item(test_client_db):
    test_client_db.post("/item/test", data={"price": 12, "store_id": 1})
    res2 = test_client_db.post("/item/test", data={"price": 13, "store_id": 2})
    assert res2.status_code == 400
    assert json.loads(res2.data) == {"message": "Item 'test' already exists."}


def test_delete_existing_item(test_client_db):
    test_client_db.post("/item/test", data={"price": 12, "store_id": 1})
    res = test_client_db.delete("item/test")
    assert res.status_code == 200
    assert json.loads(res.data) == {"message": "Item 'test' deleted successfully."}


def test_delete_nonexisting_item(test_client_db):
    res = test_client_db.delete("item/test")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Item 'test' not found."}


def test_put_existing_item(test_client_db):
    res1 = test_client_db.post("item/test", data={"price": 13, "store_id": 2})
    assert res1.status_code == 201
    res2 = test_client_db.put("item/test", data={"price": 23, "store_id": 21})
    assert res2.status_code == 200
    item = ItemModel.find_item_by_name("test")
    assert json.loads(res2.data) == item.json()


def test_put_nonexisting_item(test_client_db):
    res2 = test_client_db.put("item/test", data={"price": 23, "store_id": 21})
    assert res2.status_code == 201
    item = ItemModel.find_item_by_name("test")
    assert json.loads(res2.data) == item.json()
