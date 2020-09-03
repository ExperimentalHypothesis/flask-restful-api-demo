from flask_restful import Resource, reqparse

from models.store import StoreModel

BLANK_ERROR = "Field for '{}' cannot be blank."
SERVER_ERROR = "Server error."
NOT_FOUND_ERROR = "Store '{}' not found."
ALREADY_EXISTS_ERROR = "Store '{}' already exists."
SUCCESSFULLY_DELETED = "Store '{}' successfully deleted."


class Store(Resource):
    """ Resource for particular store """

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help=BLANK_ERROR.format("name"))

    @classmethod
    def get(cls, name: str):
        """ endpoint for getting one store """

        # try to find the store
        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": SERVER_ERROR}, 500
        if store:
            return store.json(), 200
        else:
            return {"message": NOT_FOUND_ERROR.format(name)}, 404

    @classmethod
    def post(cls, name: str):
        """ endpoint for creating new store """

        store = StoreModel.find_by_name(name)
        if store:
            return {"message": ALREADY_EXISTS_ERROR.format(name)}, 400

        # if not create new one
        new_store = StoreModel(name)
        try:
            new_store.save_to_db()
        except Exception as e:
            return {"message": SERVER_ERROR}, 500
        return new_store.json(), 201

    @classmethod
    def delete(cls, name: str):
        """ endpoint for deleting item from db """

        # try to find it
        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": SERVER_ERROR}, 500
        # if found, delete it
        if store:
            store.delete_from_db(), 200
        else:
            return {"message": NOT_FOUND_ERROR.format(name)}, 404

        return {"message": SUCCESSFULLY_DELETED.format(name)}

    # @classmethod
    # def put(cls, name: str):
    #     """ endoint for upserting item """
    #
    #     # parse the data sent
    #     data = self.parser.parse_args()  # {"name" : "Walmare"}
    #
    #     # try to find the store
    #     try:
    #         store = StoreModel.find_by_name(name)
    #     except Exception as e:
    #         return {"message": SERVER_ERROR}, 500
    #     # if found, update
    #     if store:
    #         store.name = data["name"]
    #     # if not found, create
    #     else:
    #         store = StoreModel(name)
    #     # save to db
    #     try:
    #         store.save_to_db()
    #     except Exception as e:
    #         return {"message": SERVER_ERROR}, 500
    #     # return result
    #     return store.json(), 200


class Stores(Resource):
    """ Resource for all stores """

    @classmethod
    def get(cls):
        """ endpoint for getting all stores - return ID and name """
        return {"stores": [store.json() for store in StoreModel.find_all()]}, 200
