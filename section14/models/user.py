from requests import Response, post
from typing import Dict, Union
from db import db

from flask import request, url_for

MAILGUN_DOMAIN = "sandbox6420919ab29b42289d43ff37f7689072.mailgun.org"
MAILGUN_API_KEY = "245d6d0fc380fba7fb1ad3125649ebf2-7cd1ac2b-47fb3ac2"
FROM_TITLE = "Store API"
FROM_EMAIL = "postmaster@sandbox6420919ab29b42289d43ff37f7689072.mailgun.org"

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
        # return post(
        #     f"http://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        #     auth=("api", MAILGUN_API_KEY),
        #     data={
        #         "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
        #         "to": self.email,
        #         "subject": "Registration confirmation",
        #         "text": "Please click this link: " + link,
        #     }
        # )
        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", f"{MAILGUN_API_KEY}"),
            data={"from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                  "to": self.email,
                  "subject": "Confirm email",
                  "text": "Clickni! " + link})

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
