import os, markdown

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager # will need Bearer in the header not JWT

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, Stores

from blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key = "sadaddaf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL","sqlite:///data.db")
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_SECRET_KEY"] = "asdlasdjoadosadjoifjd"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]  # no matter what thet send, they will not be allowed..


# initializing app extension
api = Api(app)
jwt = JWTManager(app) # not createing /auth endpoin


@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1:  # value hardcoded but it should be from config or elswhere
        return {"is_admin": True}
    return {"is_admin": False}
    

@jwt.token_in_blacklist_loader
def token_blacklisted_callback(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# configurations for JWT
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "Token has expored",
        "error": "token expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed",  # insteda of "msg": "Invalid header string: 'utf-8' codec can't decode byte 0x9f in position 25: invalid start byte"
        "error": "invalid token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "request does not contain an access token.",
        "error": "token missing"
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "the token is not fresh",
        "error": "fresh token required"
    }), 401

# it is sort of blacklisting ... adding to revoked token list will disable access
@jwt.revoked_token_loader
def token_revoked_callback():
    return jsonify({
        "description": "token has been revoked",
        "error": "token revoked"
    }), 401


# creating api endpoints
api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")
api.add_resource(User, "/user/<int:id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")


@app.route("/")
def index():
    """ Index route display documentation """

    with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as md:
        content = md.read()
        return markdown.markdown(content)



# when developing..
if __name__ == "__main__":

    # this will create tables in db before first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    from db import db
    db.init_app(app)
    app.run(debug=True)
