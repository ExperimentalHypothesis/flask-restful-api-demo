from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    """ Resource for one particulart item. """
     
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price of the item")
    parser.add_argument("store_id", type=int, required=True, help="ID of store where the item belogs")

    @jwt_required() # this cause that only logged in users can get the data
    def get(self, name):
        """ endpoint for getting one item by name """

        try:
            found_item = ItemModel.find_item_by_name(name)
        except:
            {"message": "error when trying to search the item" }, 500
        if found_item:
            return found_item.json(), 200 # calling the method json() from ItemModel class, because i need to return JSON, not the object instance
        return {"message": "item not found" }, 404


    def post(self, name):
        """ endponint for creating an item, it does not accept full json, but parses it and uses only {price: <float>} """

        if ItemModel.find_item_by_name(name):
            return{"message": f"item {name} already exists"}, 400 # bad request - fault of client

        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data) # data["price"], data["store_id"]

        try:
            new_item.save_to_db()
        except:
            return {"message" : "error when inserting item to database"}, 500 # internal server error
        return new_item.json(), 201

    
    def delete(self, name):
        """ endpoint for deleting an item by name """

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : f"item {name} deleted"}
        

    def put(self, name):
        """ endpoint for updating/creating an item by name """
    
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        
        if item: # updaing, if it exists
            item.price = data["price"] 
            item.store_id = data["store_id"]
        else: # creating new, if it doesnt
            item = ItemModel(name, **data) # data["price"], data["store_id"]

        item.save_to_db()
        return item.json()
            

class Items(Resource):
    """ Resource for all the items. """

    def get(self):
        """ endpoint for getting all the items """

        # items = ItemModel.query.all() # this returs list?
        return {"items" : [item.json() for item in ItemModel.query.all()]}, 200

