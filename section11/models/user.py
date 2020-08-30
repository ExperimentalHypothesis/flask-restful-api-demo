import sqlite3
from db import db

class UserModel(db.Model):
    """ Data model for creating a user """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        """ save user to db """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls, id):
        """ get user by id """
        return UserModel.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username):
        """ get user by username """
        return UserModel.query.filter_by(username=username).first()