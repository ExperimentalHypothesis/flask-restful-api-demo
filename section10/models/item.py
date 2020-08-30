from db import db

class ItemModel(db.Model):
    """ Data model representing an item """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    
    # timdle sparuju dve tabulky db.ForeignKey("stores.id") odkazuje na id v StoreModelu
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id")) 
    store = db.relationship("StoreModel") # ONE TO MANY relation = jeden store ma hode items

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def __repr__(self):
        return f"<Itemmodel {self.name}, {self.price}>"

    def json(self):
        """ make JSON frm the data, because only JSON can be returned from API """
        return  {"name": self.name, "price" : self.price, "store_id" : self.store_id}

    @classmethod
    def find_item_by_name(cls, name: str):
        """ helper method used for finding item by name, used in two methods - GET and POST"""
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
 
    def save_to_db(self):
        """ method used for updating and inserting, used in two methods - POST and PUT """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ method used for deleting from db """
        db.session.delete(self)
        db.session.commit()

    
