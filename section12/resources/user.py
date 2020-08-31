 
import sqlite3

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_refresh_token_required,
                                get_jwt_identity, jwt_required,
                                get_raw_jwt)
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", required=True, type=str)
_user_parser.add_argument("password", required=True, type=str)
 

class UserRegister(Resource):
    """ Resource for registering user. Data will come in this format {"username": "Lukas", "password" : "p@55w0rd"} """   
    
    def post(self): 
        
        data = _user_parser.parse_args()
      
        if UserModel.get_user_by_username(data["username"]): 
            return {"message" : "user already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message" : "user added succesfully"}, 201
    

class User(Resource):
    """ Resource for user. """

    @classmethod
    def get(cls, id: int):
        """ Endpoint for getting user details. """
        try:
            user = UserModel.get_user_by_id(id)
        except:
            return {"msg": "server error"}, 500
        
        if user:
            return user.json(), 200
        return {"msg": f"user with id {id} not found"}, 404

    @classmethod
    def delete(cls, id: int):
        """ Endpoint for deleting user. """
        try:
            user = UserModel.get_user_by_id(id)
        except:
            return {"msg": "server error"}

        if user:
            user.delete_from_db()
            return {"msg": "user deleted"}, 200
        return {"msg": f"user with id {id} not found"}, 404


class UserLogin(Resource):
    """ Resource for loging a user. This is basically what JWT did before in section 10. """
    
    @classmethod
    def post(cls):
        """ Create tokens for particular user. """
        
        # get data from parser
        data = _user_parser.parse_args()
        # find user in database based on username
        user = UserModel.get_user_by_username(data["username"])
        # check password - this is what the authenticate() function did in section 10
        if user and safe_str_cmp(user.password, data["password"]):
        # generate the tokens - this is what the identity() function did in section 10
            access_token = create_access_token(identity=user.id, fresh=True) # these two functions are part of JWTExtended
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200 
        return {"msg": "invalid credentials"}, 401


class UserLogout(Resource):
    """ This will blacklist specific token based on JTW id. """
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "successfully loged out"}, 200


class TokenRefresh(Resource):
    """ 
    Resource that refreshes token. 
    It generates NonFresh tokens - for instance when a user in on a page for longer 
    time as opposed to situation when he just gave the username and password.
    """

    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        print(current_user_id)

        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": new_token}, 200
         