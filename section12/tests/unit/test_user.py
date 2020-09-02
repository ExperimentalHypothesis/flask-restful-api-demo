from models.user import UserModel


def test_user_init():
    u = UserModel("test", "passwd")
    assert u.username == "test"
    assert u.password == "passwd"