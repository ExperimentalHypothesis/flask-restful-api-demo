import os, markdown

from db import db
from ma import ma
from flask import Flask, jsonify, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager  # will need Bearer in the header not JWT

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, UserConfirm
from resources.item import Item, Items
from resources.store import Store, Stores
from marshmallow import ValidationError
from blacklist import BLACKLIST


app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # no matter what they send, they will not be allowed..

api = Api(app)
jwt = JWTManager(app)  # not creating /auth endpoint


@jwt.token_in_blacklist_loader
def token_blacklisted_callback(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@app.errorhandler(ValidationError)
def handle_marshmallow_err(err):
    return jsonify(err.messages), 400


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
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

@app.route("/")
def index():
    """ Index route display documentation """
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as md:
        content = md.read()
        return markdown.markdown(content)


# this will create tables in db before first request
@app.before_first_request
def create_tables():
    db.create_all()


# when developing..
if __name__ == "__main__":

    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)
