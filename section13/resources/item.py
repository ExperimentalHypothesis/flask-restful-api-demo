from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from marshmallow import ValidationError

from models.item import ItemModel
from schemas.item import ItemSchema

SERVER_ERROR = "Server error."
NOT_FOUND_ERROR = "Item '{}' not found."
ALREADY_EXISTS_ERROR = "Item '{}' already exists."
ITEM_DELETED = "Item '{}' deleted successfully."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    """ Resource for one particular item. """

    @classmethod
    def get(cls, name: str):
        """ endpoint for getting one item by name """
        try:
            found_item = ItemModel.find_item_by_name(name)
        except:
            return {"message": SERVER_ERROR}, 500

        if found_item:
            return item_schema.dump(found_item), 200
        return {"message": NOT_FOUND_ERROR.format(name)}, 404

    @classmethod
    # @fresh_jwt_required  # this will accept only newly generated fresh token - the one you get after loging in
    def post(cls, name: str):
        """ endpoint for creating an item, it does not ac  cept full json, but parses it and uses only {price: <float>} """

        received_json = item_schema.load(request.get_json())
        received_json["name"] = name  # adding name from path to json that will be loaded

        if ItemModel.find_item_by_name(name):
            return {"message": ALREADY_EXISTS_ERROR.format(name)}, 400
        new_item = ItemModel(**received_json)

        try:
            new_item.save_to_db()
        except:
            return {"message": SERVER_ERROR}, 500
        return item_schema.dump(new_item), 201

    @classmethod
    # @jwt_required
    def delete(cls, name: str):
        """ endpoint for deleting an item by name """
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": ITEM_DELETED.format(name)}

    @classmethod
    def put(cls, name: str):
        """ endpoint for updating/creating an item by name """
        received_json = item_schema.load(request.get_json())
        received_json["name"] = name

        item = ItemModel.find_item_by_name(name)

        if item:  # updating, if it exists
            item.price = received_json["price"]
            item.store_id = received_json["store_id"]
        else:  # creating new, if it doesnt
            item = ItemModel(**received_json)
        item.save_to_db()
        return item_schema.dump(item)


class Items(Resource):
    """ Resource for all the items. """

    @classmethod
    def get(cls):
        """ endpoint for getting all the items """
        return {"items": item_list_schema.dump(ItemModel.find_all())}
