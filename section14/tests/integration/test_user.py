from models.user import UserModel
from models.confirmation import ConfirmationModel
import time


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


def test_get_latest_confirmation(test_client_db):
    # mam usera
    u = UserModel(username="test", password="passtest", email="test@test.com")
    u.save_to_db()

    # kterej udela dvakrat konfirmaci - ta druha je tedy ta nejaktualnejsi
    c1 = ConfirmationModel(1)
    time.sleep(1)
    c2 = ConfirmationModel(1)
    c1.save_to_db()
    c2.save_to_db()

    # kdyz udelam query na toho usera, tak ta pozdejsi confirmace ma spravny id.
    user = u.get_user_by_id(1)
    assert c2.id == user.get_latest_confirmation.id