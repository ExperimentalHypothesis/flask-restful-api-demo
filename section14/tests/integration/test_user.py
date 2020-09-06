from models.user import UserModel

def test_save_delete(test_client_db):
    u = UserModel(username="test", password="passtest", email="test@test.com")
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is None

    u.save_to_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is not None

    u.delete_from_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is None


def test_get_user_by_id(test_client_db):
    u = UserModel(username="test", password="passtest", email="test@test.com")
    u.save_to_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id.username == "test"
    assert found_by_id.password == "passtest"
    assert found_by_id.id == 1
