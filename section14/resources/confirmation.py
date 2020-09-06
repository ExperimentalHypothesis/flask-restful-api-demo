from flask import make_response, render_template
from flask_restful import Resource
from models.confirmation import ConfirmationModel
from models.user import UserModel
import time, traceback
from schemas.confirmation import ConfirmationSchema
from libs.mailgun import MailgunException

confirmation_schema = ConfirmationSchema()

class Confirmation(Resource):
    """ Resource for confirming user. """

    @classmethod
    def get(cls, confirmation_id: str):
        """ Return confirmation HTML page. This is what was previously done by in UserConfirm. """

        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {"message": "Confirmation reference not found"}, 404

        if confirmation.expired:
            return {"message": "Confirmation line expired"}, 400

        if confirmation.confirmed:
            return {"message": "Confirmation already done"}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=confirmation.user.username), 200, headers)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """ Returns confirmation for a given user. For testing. """
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {"message": "user does not exists"}
        return(
            {
                "curr_time": int(time.time()),
                "confirmation": [confirmation_schema.dump(i) for i in user.confirmation.order_by(ConfirmationModel.expire_at)],
            }, 200
        )

    @classmethod
    def post(cls, user_id: int):
        """ Resend confirmation email. """
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404

        try:
            confirmation = user.get_latest_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "already confirmed"}, 400
                confirmation.force_to_expire()

                new_confirmation = ConfirmationModel(user_id)
                new_confirmation.save_to_db()
                return {"message": "resend succesfull"}, 201
        except MailgunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": "resend fail"}, 500