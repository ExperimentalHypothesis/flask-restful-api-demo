from models.item import ItemModel
from schemas.item import ItemSchema
import json


def test_get_all_items_empty(test_client_db):
    res = test_client_db.get("/items")
    assert res.status_code == 200
    assert json.loads(res.data) == {"items": []}


def test_get_all_items_non_empty(test_client_db):
    i = ItemModel(name="test", price=10, store_id=1)
    i.save_to_db()
    res = test_client_db.get("/items")
    assert res.status_code == 200
    assert json.loads(res.data) == {
        "items": [{"id": 1, "name": "test", "price": 10, "store_id": 1}]
    }


def test_get_single_existing_item(test_client_db):
    i = ItemModel(name="test", price=10, store_id=1)
    i.save_to_db()
    res = test_client_db.get("/item/test")
    assert res.status_code == 200
    assert json.loads(res.data) == {"id": 1, "name": "test", "price": 10, "store_id": 1}


def test_get_single_nonexisting_item(test_client_db):
    res = test_client_db.get("/item/test")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Item 'test' not found."}


def test_post_item(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"price": 12, "store_id": 1}
    res = test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    assert res.status_code == 201  # bach na JTW REQUIRED.. musim pak dopsat
    ItemModel.find_item_by_name("test")
    assert json.loads(res.data) == {
        "id": 1,
        "name": "test",
        "price": 12,
        "store_id": 1,
    }


def test_post_duplicate_item(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"price": 12, "store_id": 1}
    res1 = test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    res2 = test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    assert res2.status_code == 400
    assert json.loads(res2.data) == {"message": "Item 'test' already exists."}


def test_delete_existing_item(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"price": 12, "store_id": 1}
    test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    res = test_client_db.delete("item/test")
    assert res.status_code == 200
    assert json.loads(res.data) == {"message": "Item 'test' deleted successfully."}


def test_delete_nonexisting_item(test_client_db):
    res = test_client_db.delete("item/test")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "Item 'test' not found."}


def test_put_existing_item(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"price": 12, "store_id": 1}
    res = test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    assert res.status_code == 201
    res2 = test_client_db.put("item/test", data=json.dumps(data), headers=headers)
    assert res2.status_code == 200
    item = ItemModel.find_item_by_name("test")
    assert json.loads(res2.data) == {
        "id": 1,
        "name": "test",
        "price": 12,
        "store_id": 1,
    }


def test_put_nonexisting_item(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"price": 12, "store_id": 1}
    res = test_client_db.post("/item/test", data=json.dumps(data), headers=headers)
    assert res.status_code == 201
    ItemModel.find_item_by_name("test")
    assert json.loads(res.data) == {
        "id": 1,
        "name": "test",
        "price": 12,
        "store_id": 1,
    }
