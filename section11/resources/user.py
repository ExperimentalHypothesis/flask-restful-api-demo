
import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    """ Endpoint for registering user. Data will come in this format {"username": "Lukas", "password" : "p@55w0rd"} """

    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str)
    parser.add_argument("password", required=True, type=str)
    
    def post(self):
        
        data = UserRegister.parser.parse_args()
      
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
            return {"user_name": f"{user.username}", "user_password": f"{user.password}"}, 200
        return {"msg": f"user with id {id} not found"}, 404

    @classmethod
    def delete(cls, id):
        """ Endpoint for deleting user. """
        try:
            user = UserModel.get_user_by_id(id)
        except:
            return {"msg": "server error"}

        if user:
            user.delete_from_db()
            return {"msg": "user deleted"}, 200
        return {"msg": f"user with id {id} not found"}, 404


