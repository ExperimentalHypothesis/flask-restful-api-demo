from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel

BLANK_ERROR = "Field for '{}' cannot be blank."
SERVER_ERROR = "Server error."
NOT_FOUND_ERROR = "Item '{}' not found."
ALREADY_EXISTS_ERROR = "Item '{}' already exists."
ITEM_DELETED = "Item '{}' deleted successfully."

class Item(Resource):
    """ Resource for one particulart item. """

    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help=BLANK_ERROR.format("price"))
    parser.add_argument("store_id", type=int, required=True, help=BLANK_ERROR.format("store_id"))

    @classmethod
    def get(cls, name: str):
        """ endpoint for getting one item by name """
        try:
            found_item = ItemModel.find_item_by_name(name)
        except:
            {"message": SERVER_ERROR}, 500
        if found_item:
            return (
                found_item.json(),
                200,
            )
        return {"message": NOT_FOUND_ERROR.format(name)}, 404

    @classmethod
    @fresh_jwt_required  # this will accept only newly generated fresh token - the one you get after loging in
    def post(cls, name: str):
        """ endponint for creating an item, it does not accept full json, but parses it and uses only {price: <float>} """
        if ItemModel.find_item_by_name(name):
            return {
                "message": ALREADY_EXISTS_ERROR.format(name)
            }, 400  # bad request - fault of client

        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)  # data["price"], data["store_id"]

        try:
            new_item.save_to_db()
        except:
            return {
                "message": SERVER_ERROR
            }, 500  # internal server error
        return new_item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        """ endpoint for deleting an item by name """
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": ITEM_DELETED.format(name)}

    @classmethod
    def put(cls, name: str):
        """ endpoint for updating/creating an item by name """
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item:  # updaing, if it exists
            item.price = data["price"]
            item.store_id = data["store_id"]
        else:  # creating new, if it doesnt
            item = ItemModel(name, **data)  # data["price"], data["store_id"]
        item.save_to_db()
        return item.json()


class Items(Resource):
    """ Resource for all the items. """

    @classmethod
    def get(cls):
        """ endpoint for getting all the items """
        return {"items": [item.json() for item in ItemModel.find_all()]}
