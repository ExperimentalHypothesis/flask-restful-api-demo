import os, markdown

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager # will need Bearer in the header not JWT

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.secret_key = "sadaddaf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL","sqlite:///data.db")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "asdlasdjoadosadjoifjd"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# initializing app extension
api = Api(app)
jwt = JWTManager(app) # not createing /auth endpoin


@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1:  # value hardcoded but it should be from config or elswhere
        return {"is_admin": True}
    return {"is_admin": False}
    

# creating api endpoints
api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")
api.add_resource(User, "/user/<int:id>")
api.add_resource(UserLogin, "/login")
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
