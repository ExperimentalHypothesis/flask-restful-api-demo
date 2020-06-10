
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
            return {"message" : f"user {data['username']} already exists"}, 400

        # user = UserModel(data["username"], data["password"])
        user = UserModel(**data)

        user.save_to_db()

        return {"message" : f"user {data['username']} added succesfully"}, 201
            

