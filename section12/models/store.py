from typing import Dict, List, Union

from db import db
from models.item import ItemJSON

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]

class StoreModel(db.Model):
    """ Data model for a store """

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    items = db.relationship("ItemModel", lazy="dynamic") # tohle vrati list query builder, kdyz to nechci vytvaret hned

    def __init__(self, name: str):
        self.name = name 

    def __repr__(self) -> Dict:
        return f"<StoreModel {self.id}, {self.name}>"

    def json(self) -> StoreJSON:
        """ make JSON frm the data, because only JSON can be returned from API """
        return {"id" : self.id, 
                "name" : self.name, 
                "items": [item.json() for item in self.items.all()]} # kdyz mam lazy tak tady musim data all.. list se vytvori az na zavolani.. 
    
    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        """ helper method used for finding item by name, used in two methods - GET and POST"""
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        """ helper method used for getting all stores. """
        return cls.query.all()

    def save_to_db(self) -> None:
        """ save store to db """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """ delete store from db """
        db.session.delete(self)
        db.session.commit()

