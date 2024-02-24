from flask import Flask, request, jsonify
from pymongo import MongoClient

class UserAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['BMS_DB']

    def run(self):
        @self.app.route('/user_info', methods=['POST'])
        def get_user_info():
            data = request.get_json()

            # Check if all required fields are present
            if 'name' not in data or 'order' not in data or 'address' not in data or 'phone_number' not in data:
                return jsonify({'error': 'Missing required fields'}), 400

            name = data['name']
            order = data['order']
            address = data['address']
            phone_number = data['phone_number']

            # Store user information in MongoDB
            collection_name = f"bms_col_{name}"  # Dynamically generate collection name
            user_collection = self.db[collection_name]
            user_collection.insert_one({
                'name': name,
                'order': order,
                'address': address,
                'phone_number': phone_number
            })

            return jsonify({'message': 'User information received and stored successfully'}), 200

        @self.app.route('/get_user_info', methods=['GET'])
        def return_user_info():
            data = request.get_json()
            if 'name' not in data:
                return jsonify({'error': 'Name not provided in the request'}), 400

            name = data['name']
            collection_name = f"bms_col_{name}"  # Dynamically generate collection name
            user_collection = self.db[collection_name]
            user_data = user_collection.find_one({})
            if not user_data:
                return jsonify({'error': 'No user information available'}), 404

            return jsonify(user_data), 200

        self.app.run(debug=True)
