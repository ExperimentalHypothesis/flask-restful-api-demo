from app import app
from db import db

db.init_app(app)

# this will create tables in db before first request
@app.before_first_request
def create_tables():
    db.create_all()
