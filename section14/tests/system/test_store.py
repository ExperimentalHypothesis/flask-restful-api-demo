from models.store import StoreModel
from models.item import ItemModel
import json


def test_get_all_stores_empty(test_client_db):
    res = test_client_db.get("/stores")
    assert res.status_code == 200
    assert json.loads(res.data) == {"stores": []}


def test_get_all_stores_nonempty(test_client_db):
    s = StoreModel(name="test")
    s.save_to_db()
    res = test_client_db.get("/stores")
    found_store = StoreModel.find_by_name("test")
    assert res.status_code == 200
    assert json.loads(res.data) == {"stores": [{"id": 1, "items": [], "name": "test"}]}


def test_get_one_existing_store(test_client_db):
    s = StoreModel(name="teststore")
    s.save_to_db()
    i = ItemModel(name="testitem", price=10, store_id=1)
    i.save_to_db()
    found_store = StoreModel.find_by_name("teststore")
    res = test_client_db.get("/store/teststore")
    assert res.status_code == 200
    assert json.loads(res.data) == {
        "id": 1,
        "name": "teststore",
        "items": [{"id": 1, "name": "testitem", "price": 10.0, "store_id": 1}],
    }


def test_get_one_nonexisting_store(test_client_db):
    res = test_client_db.get("/store/teststore")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Store 'teststore' not found."}


def test_post_store(test_client_db):
    res = test_client_db.post("/store/teststore")
    assert res.status_code == 201
    assert json.loads(res.data) == {"id": 1, "name": "teststore", "items": []}


def test_post_duplicate_store(test_client_db):
    test_client_db.post("/store/teststore")
    res = test_client_db.post("/store/teststore")
    assert res.status_code == 400
    assert json.loads(res.data) == {"message": "Store 'teststore' already exists."}


def test_delete_existing_store(test_client_db):
    test_client_db.post("/store/teststore")
    res = test_client_db.delete("/store/teststore")
    assert res.status_code == 200
    assert json.loads(res.data) == {
        "message": "Store 'teststore' successfully deleted."
    }


def test_delete_nonexisting_store(test_client_db):
    res = test_client_db.delete("/store/teststore")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Store 'teststore' not found."}
