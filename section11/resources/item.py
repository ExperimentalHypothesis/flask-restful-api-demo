from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel


class Item(Resource):
    """ Resource for one particulart item. """
     
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="price of the item")
    parser.add_argument("store_id", type=int, required=True, help="ID of store where the item belogs")

    @jwt_required # no bracktes if i use JWT extended - it can be fresh or non fresh token..
    def get(self, name):
        """ endpoint for getting one item by name """

        try:
            found_item = ItemModel.find_item_by_name(name)
        except:
            {"message": "error when trying to search the item" }, 500
        if found_item:
            return found_item.json(), 200 # calling the method json() from ItemModel class, because i need to return JSON, not the object instance
        return {"message": "item not found" }, 404


    @fresh_jwt_required # this will accept only newly generated fresh token - the one you get after loging in
    def post(self, name): 
        """ endponint for creating an item, it does not accept full json, but parses it and uses only {price: <float>} """

        if ItemModel.find_item_by_name(name):
            return{"message": "item already exists"}, 400 # bad request - fault of client

        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data) # data["price"], data["store_id"]

        try:
            new_item.save_to_db()
        except:
            return {"message" : "error when inserting item to database"}, 500 # internal server error
        return new_item.json(), 201


    @jwt_required
    def delete(self, name):
        """ endpoint for deleting an item by name """

        # delete only if you are admin
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"msg": "you must be admin"}

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "item deleted"}
        

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

    @jwt_optional # JWT can either be passed or not - user is logged or not
    def get(self):
        """ endpoint for getting all the items """
        user_id = get_jwt_identity() # returns ID or none
        print(user_id)

        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200   # if he provides, return all
        return {
                "items" : [item.name for item in ItemModel.find_all()],
                "msg": "more data available if you log in"}, 200  # if not, return only names
