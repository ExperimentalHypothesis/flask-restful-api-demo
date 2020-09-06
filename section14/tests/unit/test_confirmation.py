from models.confirmation import ConfirmationModel
import time


def test_confirmation_init():
    c = ConfirmationModel(1)
    assert c.user_id == 1
    assert c.confirmed is False
    assert type(c.id) != ''
    assert c.expire_at > time.time()
    assert c.expired is False


