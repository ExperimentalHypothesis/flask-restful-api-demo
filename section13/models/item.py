from typing import Dict, List, Union

from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    """ Data model representing an item """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    price = db.Column(db.Float(precision=2), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __repr__(self):
        return f"<ItemModel {self.name}, {self.price}>"

    @classmethod
    def find_item_by_name(cls, name: str) -> "ItemModel":
        """ helper method used for finding item by name, used in two methods - GET and POST"""
        return cls.query.filter_by(
            name=name
        ).first()  # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        """ helper method used for getting all items. """
        return cls.query.all()

    def save_to_db(self) -> None:
        """ method used for updating and inserting, used in two methods - POST and PUT """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """ method used for deleting from db """
        db.session.delete(self)
        db.session.commit()
