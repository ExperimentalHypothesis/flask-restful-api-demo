from models.confirmation import ConfirmationModel


def test_save_to_db(test_client_db):
    c = ConfirmationModel(1)
    assert ConfirmationModel.find_by_id(c.id) is None

    c.save_to_db()
    assert ConfirmationModel.find_by_id(c.id) is not None


def test_delete_from(test_client_db):
    c = ConfirmationModel(1)
    assert ConfirmationModel.find_by_id(c.id) is None

    c.save_to_db()
    assert ConfirmationModel.find_by_id(c.id) is not None

    c.delete_from_db()
    assert ConfirmationModel.find_by_id(c.id) is None


def test_force_to_expire(test_client_db):
    c = ConfirmationModel(1)
    assert c.expired is False
    c.force_to_expire()
    assert c.expired is True
