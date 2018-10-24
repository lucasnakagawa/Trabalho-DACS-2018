from bson.objectid import ObjectId
from client import Client
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://172.18.0.35:27017/DBlucasnakagawa"
mongo = PyMongo(app)

@app.route('/api/v1.0/client', methods=['GET'])
def get_tasks():
    clients = []
    for client in mongo.db.clients.find():
        new_client = Client()
        new_client._id = str(client['_id'])
        new_client.name = client['name']
        new_client.phone = client['phone']
        new_client.email = client['email']
        clients.append(new_client)

    return jsonify([client.__dict__ for client in clients]), 201

@app.route('/api/v1.0/clients', methods=['POST'])
def create_client():
    new_client = Client()
    new_client._id = ObjectId()
    new_client.name = request.json['name']
    new_client.phone = request.json['phone']
    new_client.email = request.json['email']

    ret = mongo.db.clients.insert_one(new_client.__dict__).inserted_id
    return jsonify({'id': str(ret)}), 201

@app.route('/api/v1.0/client/<string:_id>', methods=['PUT'])
def update_client(_id):
    updated_client = Client()
    updated_client._id = ObjectId(_id)
    updated_client.name = request.json['name']
    updated_client.phone = request.json['phone']
    updated_client.email = request.json['email']

    mongo.db.clients.update_one({'_id': updated_client._id},
                                {'$set': updated_client.__dict__},
                                upsert=False)

    return jsonify({'id': str(update_client._id)}), 201

@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_client(_id):
    _id = ObjectId(_id)
    ret = mongo.db.clients.delete_one({'_id': _id}).deleted_count
    return jsonify({'delete_count': str(ret)}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
