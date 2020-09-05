from requests import Response, post
from typing import Dict, Union
from db import db

from flask import request, url_for
from libs.mailgun import Mailgun


UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    """ Data model for creating a user """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    def save_to_db(self) -> None:
        """ save user to db """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_confirmation_email(self) -> Response:
        """ This function will talk to Mailgun. """
        # build the link the user will click on,
        # it should be http://localhost:5000/user_confirm/1)
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        email = self.email
        subject = "Confirm Registeration"
        text = f"Please click this link: {link}"
        Mailgun.send_email(email, subject, text)


    @classmethod
    def get_user_by_id(cls, id: int) -> "UserModel":
        """ get user by id """
        return UserModel.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username) -> "UserModel":
        """ get user by username """
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email) -> "UserModel":
        """ get user by username """
        return UserModel.query.filter_by(email=email).first()
