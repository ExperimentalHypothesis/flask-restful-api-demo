from models.user import UserModel
import json, os

import pytest
from app import app
from db import db


@pytest.fixture(autouse=True)
def test_client_db():

    # set up
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    app.config["JWT_SECRET_KEY"] = "testing"

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
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd", "email": "kotatko.lukas@gmail.com"}
    res = test_client_db.post("/register", data=json.dumps(data), headers=headers)
    assert res.status_code == 201
    # assert json.loads(res.data) == {"message": "User '{}' added successfully. Email was send to confirm you identity".format("testname")}
    #
    # new_user = UserModel.get_user_by_username("testname")
    # assert new_user is not None
    # assert new_user.username == "testname"
    # assert new_user.password == "testpwd"


def test_register_duplicated_user(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd", "email": "kotatko.lukas@gmail.com"}
    res = test_client_db.post("/register", data=json.dumps(data), headers=headers)
    res = test_client_db.post("/register", data=json.dumps(data), headers=headers)
    assert res.status_code == 400
    assert json.loads(res.data) == {"message": "User 'testname' already exists."}


def test_get_existing_user(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd", "email": "kotatko.lukas@gmail.com"}
    res = test_client_db.post("/register", data=json.dumps(data), headers=headers)
    assert res.status_code == 201
    res = test_client_db.get("user/1")
    assert res.status_code == 200
    assert json.loads(res.data) == {"id":1,
                                    "username": "testname",
                                    "email": "kotatko.lukas@gmail.com"
                                    }


def test_get_nonexisting_user(test_client_db):
    res = test_client_db.get("user/1")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": "User '1' not found."}


def test_delete_existing_user(test_client_db):
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd",  "email": "kotatko.lukas@gmail.com"}
    res = test_client_db.post("/register", data=json.dumps(data), headers=headers)
    assert res.status_code == 201
    res = test_client_db.delete("user/1")
    assert res.status_code == 200
    assert json.loads(res.data) == {"msg": "User '1' deleted successfully."}


def test_delete_nonexisting_user(test_client_db):
    res = test_client_db.delete("user/1")
    assert res.status_code == 404
    assert json.loads(res.data) == {"msg": "User '1' not found."}


def test_user_valid_login(test_client_db):
    # register a user
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd", "email": "kotatko.lukas@gmail.com"}
    test_client_db.post("/register", data=json.dumps(data), headers=headers)

    # confirm the user
    test_client_db.get("/user_confirm/1")

    # login the user
    res = test_client_db.post("login", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert "access_token" in json.loads(res.data)
    assert "refresh_token" in json.loads(res.data)
    assert json.loads(res.data)["access_token"] != ""
    assert json.loads(res.data)["refresh_token"] != ""


def test_existing_user_confirm(test_client_db):
    # register
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd",  "email": "kotatko.lukas@gmail.com"}
    test_client_db.post("/register", data=json.dumps(data), headers=headers)

    # activate the existing user
    res = test_client_db.get("/user_confirm/1")
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "text/html"
    assert b"Your registration has been confirmed through" in res.data


def test_nonexisting_user_confirm(test_client_db):
    res = test_client_db.get("/user_confirm/1")
    assert res.status_code == 404
    assert json.loads(res.data) == {"message": "User '1' not found."}


def test_user_not_confirmed_login(test_client_db):
    # register
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd",  "email": "test@test.com"}
    test_client_db.post("/register", data=json.dumps(data), headers=headers)

    # registered (but not activated) tries to log in
    res = test_client_db.post("/login", data=json.dumps(data), headers=headers)
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}


def test_user_invalid_credentials_login(test_client_db):
    # try to login without being registered
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd",  "email": "test@test.com"}
    res = test_client_db.post("login", data=json.dumps(data), headers=headers)
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}

    # try to login with wrong username
    test_client_db.post("register", data=json.dumps(data), headers=headers)
    res = test_client_db.post(
        "login", data=json.dumps({"username": "testnamewrong", "password": "testpwd"}), headers=headers)
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}

    # try to login with wrong pssword
    res = test_client_db.post("login",
                              data=json.dumps({"username": "testname", "password": "testpwdwrong"}),
                              headers=headers)
    assert res.status_code == 401
    assert json.loads(res.data) == {"msg": "Invalid credentials."}


def test_user_logout(test_client_db):
    # create a user
    UserModel(username="testname", password="testpwd", email="test@test.com").save_to_db()
    # confirm the user
    test_client_db.get("/user_confirm/1")
    # login
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd"}
    auth_res = test_client_db.post("login", data=json.dumps(data), headers=headers)
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
    UserModel(username="testname", password="testpwd", email="test@test.com").save_to_db()
    # confirm the user
    test_client_db.get("/user_confirm/1")
    # kterej se logne
    headers = {"content-type": "application/json"}
    data = {"username": "testname", "password": "testpwd"}
    auth_res = test_client_db.post("login", data=json.dumps(data), headers=headers)
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
