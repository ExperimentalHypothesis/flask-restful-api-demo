import os
from requests import Response, post
from typing import List


class MailgunException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Mailgun:
    """ Class handling sending emails. """

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Store API"
    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str) -> Response:
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException("no domain")
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException("no api")

        response = post(f"https://api.mailgun.net/v3/sandbox6420919ab29b42289d43ff37f7689072.mailgun.org/messages",
            auth=("api", f"245d6d0fc380fba7fb1ad3125649ebf2-7cd1ac2b-47fb3ac2"),
            data={"from": f"{cls.FROM_TITLE} <some@user.com>",
                  "to": email,
                  "subject": subject,
                  "text": text})

        if response.status_code != 200:
            raise MailgunException("Email not sent.")

        return response
