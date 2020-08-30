# from werkzeug import  safe_str_cmp
from models.user import UserModel
 

# this is how the authentication works:

# step 1]
# this function is used by JWT in /auth endpoint when i am sending the json data = eg:
# {
# 	"username": "lukas",
# 	"password": "ahoj"
# }
# it will check if the user is in the db and returns the user back.. simple enought
def authenticate(username, password):
    user = UserModel.get_user_by_username(username)
    if user and user.password == password:
        return user

# step 2] 
# JWT will create a token, something like: adlka  jkljdposajhfaijdaposjdaodjasidhsaidjsadsabksjd
# in this token it saves some data, it stores user's id (encrypted)
# it is saved as the 'identity' key in the JWS so when we decrypt it

# so step 3] 
# when the JWT token is send as payload, it parses out the payload['identity'] 
# which is the id of a user and search for this user based on it
def identify(payload):
    user_id = payload["identity"]
    return UserModel.get_user_by_id(user_id)


# FLASK JWT_EXTENDED IS MORE EXPLICIT.. 