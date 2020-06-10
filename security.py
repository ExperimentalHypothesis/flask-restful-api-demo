# from werkzeug import  safe_str_cmp
from models.user import UserModel
 

def authenticate(username, password):
    
    user = UserModel.get_user_by_username(username)
    if user and user.password == password:
        return user


def identify(payload):

    user_id = payload["identity"]
    return UserModel.get_user_by_id(user_id)
