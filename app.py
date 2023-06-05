from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    store_name = db.Column(db.String(64), index=True)
    store_address = db.Column(db.String(128), unique=True, index=True)
    price = db.Column(db.String(16))
    package_left = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    pick_up_time = db.Column(db.String(32))
    data = db.Column(db.String(4096))

    def __repr__(self):
        return f"{self.store_name} - {self.store_address} - {self.price} - {self.package_left} - {self.pick_up_time}"


class GetStore(Resource):

    def get(self, id):
            stores = Store.query.get(id)
            if stores is None:
                return {'error': 'store not found'}, 404
            data = {"store_id": stores.store_id, "store_name": stores.store_name, "store_address": stores.store_address,
                    "price": stores.price, "package_left": stores.package_left, "is_active": stores.is_active,
                    "pick_up_time": stores.pick_up_time}
            return {"code": 200, "Store": data}

class GetAllStores(Resource):

    def get(self):
        stores = Store.query.all()
        store_list = []
        for s in stores:
            data = {"store_id": s.store_id, "store_name": s.store_name, "store_address": s.store_address,
                    "price": s.price, "package_left": s.package_left, "is_active": s.is_active,
                    "pick_up_time": s.pick_up_time, "data": s.data}
            store_list.append(data)
        return {"code": 200, "Stores": store_list}


class AddStore(Resource):

    def post(self):
        if request.is_json:
            store = Store(store_name=request.json["store_name"], store_address=request.json["store_address"],
                          price=request.json["price"], package_left=request.json["package_left"], is_active=True,
                          pick_up_time=request.json["pick_up_time"], data=request.json["data"])
            db.session.add(store)
            db.session.commit()
            return make_response(jsonify({"code": 200,
                "store": {"store_id": store.store_id, "store_name": store.store_name, "store_address": store.store_address,
                 "price": store.price, "package_left": store.package_left, "is_active": store.is_active,
                 "pick_up_time": store.pick_up_time}}))
        else:
            return {"code": 400, "error": "Request is not in Json format"}


class DeleteStore(Resource):

    def post(self):
        if request.is_json:
            store = Store.query.get(request.json["store_id"])
            if store is None:
                return {"code": 404, 'error': 'store not found'}
            else:
                store.is_active = False
                db.session.commit()
                return {"code": 200, "message": "Deleted"}
        else:
            return {"code": 400, "error": "Request is not in Json format"}


api.add_resource(GetAllStores, '/get_stores')
api.add_resource(GetStore, '/get_stores/<int:id>')
api.add_resource(AddStore, '/add_store')
api.add_resource(DeleteStore, '/delete_store')

# driver function
if __name__ == '__main__':
    app.run(debug=True)
