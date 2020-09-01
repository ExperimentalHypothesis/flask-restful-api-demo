from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    """ Resource for particular store """

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="name of the store")

    def get(self, name: str):
        """ endpoint for getting one store """

        # try to find the store
        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": "error occured when finding store"}, 500
        # if found, return it
        if store:
            return store.json(), 200
        # i not found, return 404
        else:
            return {"message": "store not found"}, 404

    def post(self, name: str):
        """ endpoint for creating new store """

        # parse the data sent
        # data = self.parser.parse_args() # {"name" : "WallMart"}

        # check if the store exists already
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "store with name already exists"}, 400

        # if not create new one
        new_store = StoreModel(name)
        # save to db
        try:
            new_store.save_to_db()
        except Exception as e:
            return {"message": "error when adding to db"}, 500
        # return result
        return new_store.json(), 201

    def delete(self, name: str):
        """ endpoint for deleting item from db """

        # try to find it
        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": "error  when finding the store"}
        # if found, delete it
        if store:
            store.delete_from_db(), 200
        else:
            return {"message": "store not found"}, 404

        return {"message": "item deleted"}

    def put(self, name: str):
        """ endoint for upserting item """

        # parse the data sent
        data = self.parser.parse_args()  # {"name" : "Walmare"}

        # try to find the store
        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            return {"message": "error {e} when finding the store"}, 500
        # if found, update
        if store:
            store.name = data["name"]
        # if not found, create
        else:
            store = StoreModel(name)
        # save to db
        try:
            store.save_to_db()
        except Exception as e:
            return {"message": "error {e} when saving to db"}, 500
        # return result
        return store.json(), 200


class Stores(Resource):
    """ Resource for all stores """

    def get(self):
        """ endpoint for getting all stores - return ID and name """

        # find_all() encapsulates the query object, resource should not interact with database at all
        return {"stores": [store.json() for store in StoreModel.find_all()]}, 200
