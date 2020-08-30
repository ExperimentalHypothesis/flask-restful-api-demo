from db import db

class StoreModel(db.Model):
    """ Data model for a store """

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic") # tohle vrati list query builder, kdyz to nechci vytvaret hned

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<StoreModel {self.id}, {self.name}>"

    def json(self):
        """ make JSON frm the data, because only JSON can be returned from API """
        return {"id" : self.id, 
                "name" : self.name, 
                "items": [item.json() for item in self.items.all()]} # kdyz mam lazy tak tady musim data all.. list se vytvori az na zavolani.. 
    
    @classmethod
    def find_by_name(cls, name: str):
        """ helper method used for finding item by name, used in two methods - GET and POST"""
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls):
        """ helper method used for getting all stores. """
        return cls.query.all()

    def save_to_db(self):
        """ save store to db """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ delete store from db """
        db.session.delete(self)
        db.session.commit()

