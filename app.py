from flask import Flask, jsonify, request
from db import insert_sql, execute_raw_query
from flask_cors import CORS
from dotenv import load_dotenv
import json
from util.encryption import encrypt_data, decrypt_data

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/all-tenants')
def getAllTenats():
    with open('./util/data/licence.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/audit-licence')
def getAllAuditTenats():
    with open('./util/data/licenceAudit.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


@app.route('/input-fields')
def getInputFields():
     return jsonify({
         "name": "soni"
     })

@app.route('/update-user-response', methods=['POST'])
def update_user_response():
    request_data = request.get_json()
    encrypted_data = encrypt_data(str(request_data))
    insert_sql("user_response_data", {"response": encrypted_data}) 
    return jsonify({'message': 'Request received'}), 200

@app.route('/get-user-response/<int:user_id>', methods=['GET'])
def get_user_response(user_id):
    query = f"SELECT * FROM user_response_data WHERE id = {user_id}"
    userData = execute_raw_query(query)
    
    if not userData:
        return jsonify({'error': 'User not found'}), 404

    # Decrypt the data before returning
    decrypted_data =  decrypt_data(userData[0]["response"]) 
    
    return decrypted_data

if __name__ == '__main__':
    app.run(debug=True, port=5001)
