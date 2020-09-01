from typing import Dict, Union
import sqlite3
from db import db

UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    """ Data model for creating a user """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_db(self) -> None:
        """ save user to db """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> UserJSON:
        return {"id": self.id, "username": self.username}

    @classmethod
    def get_user_by_id(cls, id: int) -> "UserModel":
        """ get user by id """
        return UserModel.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username) -> "UserModel":
        """ get user by username """
        return UserModel.query.filter_by(username=username).first()
