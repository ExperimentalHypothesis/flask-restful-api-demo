import os


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# custom imports
from security import authenticate, identify
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

# initializing main app
app = Flask(__name__)
app.secret_key = "sadaddaf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL","sqlite:///data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# initializing app extension
api = Api(app)
jwt = JWT(app, authenticate, identify) # JWT create a new endpoint /auth 

# creating api endpoints
api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")


# when developing..
if __name__ == "__main__":

    # this will create tables in db before first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    from db import db
    db.init_app(app)
    app.run(debug=True)
