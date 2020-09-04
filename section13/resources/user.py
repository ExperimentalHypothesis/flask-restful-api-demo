from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError

ALREADY_EXISTS_ERROR = "User '{}' already exists."
SUCCESSFULLY_ADDED = "User '{}' added successfully."
SUCCESSFULLY_DELETED = "User '{}' deleted successfully."
SUCCESSFULLY_LOGOUT = "Successfully loged out 'id={user_id}'."
SERVER_ERROR = "Server error."
NOT_FOUND_ERROR = "User '{}' not found."
INVALID_CREDENTIALS_ERROR = "Invalid credentials."

user_schema = UserSchema()


class UserRegister(Resource):
    """ Resource for registering user. Data will come in this format {"username": "Lukas", "password" : "p@55w0rd"} """

    @classmethod
    def post(cls):
        # tady by se to melo nejak loadnout aby se z toho hned udelal objekt user_model, ale nefunguje to nechava dict
        # co ale dela je ze checkuje argumenty, jestli sedej s modelem..
        user_model = user_schema.load(request.get_json())
        print(user_model, type(user_model))
        if UserModel.get_user_by_username(user_model["username"]):
            return {"message": ALREADY_EXISTS_ERROR.format(user_model["username"])}, 400

        user_model = UserModel(**user_model)
        user_model.save_to_db()

        return {"message": SUCCESSFULLY_ADDED.format(user_model.username)}, 201


class User(Resource):
    """ Resource for user. """

    @classmethod
    def get(cls, id: int):
        """ Endpoint for getting user details. """
        try:
            user = UserModel.get_user_by_id(id)
        except:
            return {"msg": SERVER_ERROR}, 500

        if user:
            return (
                user_schema.dump(user),
                200,
            )  # the has not changed with flask-marshmallow
        return {"msg": NOT_FOUND_ERROR.format(id)}, 404

    @classmethod
    def delete(cls, id: int):
        """ Endpoint for deleting user. """
        try:
            user = UserModel.get_user_by_id(id)
        except:
            return {"msg": SERVER_ERROR}

        if user:
            user.delete_from_db()
            return {"msg": SUCCESSFULLY_DELETED.format(id)}, 200
        return {"msg": NOT_FOUND_ERROR.format(id)}, 404


class UserLogin(Resource):
    """ Resource for logging a user. This is basically what JWT did before in section 10. """

    @classmethod
    def post(cls):
        """ Create tokens for particular user. """
        user_model = user_schema.load(request.get_json())
        user = UserModel.get_user_by_username(user_model["username"])
        if user and safe_str_cmp(user.password, user_model["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"msg": INVALID_CREDENTIALS_ERROR}, 401


class UserLogout(Resource):
    """ This will blacklist specific token based on JTW id. """

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": SUCCESSFULLY_LOGOUT.format(user_id=user_id)}, 200


class TokenRefresh(Resource):
    """
    Resource that refreshes token.
    It generates NonFresh tokens - for instance when a user in on a page for longer
    time as opposed to situation when he just gave the username and password.
    """

    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user_id = get_jwt_identity()
        print(current_user_id)

        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": new_token}, 200
