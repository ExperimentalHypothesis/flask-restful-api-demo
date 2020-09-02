from flask_restful import Resource, reqparse
from flask import request
from models.store import StoreModel
from schemas.store import StoreSchema

BLANK_ERROR = "Field for '{}' cannot be blank."
SERVER_ERROR = "Server error."
NOT_FOUND_ERROR = "Store '{}' not found."
ALREADY_EXISTS_ERROR = "Store '{}' already exists."
SUCCESSFULLY_DELETED = "Store '{}' successfully deleted."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    """ Resource for particular store """

    @classmethod
    def get(cls, name: str):
        """ endpoint for getting one store """
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {"message": SERVER_ERROR}, 500
        if store:
            return store_schema.dump(store), 200
        else:
            return {"message": NOT_FOUND_ERROR.format(name)}, 404

    @classmethod
    def post(cls, name: str):
        """ endpoint for creating new store """

        store = StoreModel.find_by_name(name)

        if store:
            return {"message": ALREADY_EXISTS_ERROR.format(name)}, 400

        # if not create new one
        new_store = StoreModel(name=name)
        try:
            new_store.save_to_db()
        except:
            return {"message": SERVER_ERROR}, 500
        return store_schema.dump(new_store), 201

    @classmethod
    def delete(cls, name: str):
        """ endpoint for deleting item from db """

        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": SERVER_ERROR}
        # if found, delete it
        if store:
            store.delete_from_db(), 200
        else:
            return {"message": NOT_FOUND_ERROR.format(name)}, 404

        return {"message": SUCCESSFULLY_DELETED.format(name)}

    @classmethod
    def put(cls, name: str):
        """ endoint for upserting item """

        received_json = request.get_json()

        try:
            store = StoreModel.find_by_name(name)
        except:
            return {"message": SERVER_ERROR}, 500

        if store:
            store.name = received_json["name"]
        else:
            store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": SERVER_ERROR}, 500
        return store_schema.dump(store), 200


class Stores(Resource):
    """ Resource for all stores """

    @classmethod
    def get(cls):
        """ endpoint for getting all stores - return ID and name """

        # find_all() encapsulates the query object, resource should not interact with database at all
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200
