from models.user import UserModel
from werkzeug.security import safe_str_cmp

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


def test_register_new_user(test_client_db):
    new_user = UserModel.get_user_by_username("testname")
    assert new_user is None

    res = test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 201
    assert json.loads(res.data) == {"message": "User 'testname' added successfully."}

    new_user = UserModel.get_user_by_username("testname")
    assert new_user is not None
    assert new_user.username == "testname"
    assert new_user.password == "testpwd"


def test_register_duplicated_user(test_client_db):
    test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    res = test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 400
    assert json.loads(res.data) == {"message": "User 'testname' already exists."}


def test_get_existing_user(test_client_db):
    res = test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 201
    res = test_client_db.get("user/1")
    assert res.status_code == 200
    assert json.loads(res.data) == UserModel.get_user_by_username("testname").json()


def test_get_nonexisting_user(test_client_db):
    res = test_client_db.get("user/1")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": "User '1' not found."}


def test_delete_existing_user(test_client_db):
    res = test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 201
    res = test_client_db.delete("user/1")
    assert res.status_code == 200
    assert json.loads(res.data) == {"msg": "User '1' deleted successfully."}


def test_delete_nonexisting_user(test_client_db):
    res = test_client_db.delete("user/1")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": "User '1' not found."}


def test_user_valid_login(test_client_db):
    test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    user_from_db = UserModel.get_user_by_username("testname")

    res = test_client_db.post(
        "login", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 200
    assert "access_token" in json.loads(res.data)
    assert "refresh_token" in json.loads(res.data)
    assert json.loads(res.data)["access_token"] != ""
    assert json.loads(res.data)["refresh_token"] != ""


def test_user_invalid_login(test_client_db):
    res = test_client_db.post(
        "login", data={"username": "testname", "password": "testpwd"}
    )
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}

    test_client_db.post(
        "register", data={"username": "testname", "password": "testpwd"}
    )
    res = test_client_db.post(
        "login", data={"username": "testnamewrong", "password": "testpwd"}
    )
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}

    res = test_client_db.post(
        "login", data={"username": "testname", "password": "testpwdwrong"}
    )
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}


def test_user_logout(test_client_db):
    # mam nejakyho usera
    UserModel("testname", "testpwd").save_to_db()
    # kterej se logne
    auth_res = test_client_db.post(
        "login", data={"username": "testname", "password": "testpwd"}
    )
    assert auth_res.status_code == 200
    # ziskam token kterej mi to vrati v responsi
    auth_token = json.loads(auth_res.data)["access_token"]

    # a pridam ho do hlavicky pri requestu na zamceny routy..
    res = test_client_db.post(
        "logout", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert res.status_code == 200
    assert json.loads(res.data) == {"message": "Successfully loged out 'id=1'."}

    # test jestli jde vylogovat se podruhy
    res = test_client_db.post(
        "logout", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Token has been revoked"}

    # test jestli se vyloguje kdy neposle header Authorization
    res = test_client_db.post("logout")
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Missing Authorization Header"}


def test_refresh_token(test_client_db):
    # mam nejakyho usera
    UserModel("testname", "testpwd").save_to_db()
    # kterej se logne
    auth_res = test_client_db.post(
        "login", data={"username": "testname", "password": "testpwd"}
    )
    # ziskam jeho refresh token
    refresh_token = json.loads(auth_res.data)["refresh_token"]
    # kterej poslu v headru na tu routu
    res = test_client_db.post(
        "refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert res.status_code == 200
    assert json.loads(res.data)["access_token"] != ""

    # kdyz ho tam neposlu..
    res = test_client_db.post("refresh")
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Missing Authorization Header"}

    # kdyz ho tam poslu ale spatnej
    res = test_client_db.post("refresh", headers={"Authorization": f"Bearer nonsense"})
    assert res.status_code == 422
    assert json.loads(res.data) == {"msg": "Not enough segments"}
