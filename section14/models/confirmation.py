from db import db
import time
from uuid import uuid4

TIME_EXP_DELTA = 1800


class ConfirmationModel(db.Model):
    """ Datamodel for confirmation. """

    __tablename__ = "confirmations"

    id = db.Column(db.String, primary_key=True)  # primary key je string !!
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time.time()) + TIME_EXP_DELTA
        self.confirmed = False

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self):
        return time.time() > self.expire_at

    def force_to_expire(self):
        if not self.expired:
            self.expire_at = int(time.time())
            self.save_to_db()



