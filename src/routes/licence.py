from flask import Blueprint, jsonify, request
import json
from src.db.dbconnection import execute_raw_query, insert_sql
from src.util.encryption import encrypt_data, decrypt_data

licenceBP = Blueprint('licence', __name__)


@licenceBP.route('/all-tenants')
def getAllTenats():
    with open('./src//util/data/licence.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@licenceBP.route('/audit-licence')
def getAllAuditTenats():
    with open('./src//util/data/licenceAudit.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


@licenceBP.route("/refresh-licence",methods=['POST'])
def refreshLicence():
    pass

@licenceBP.route("/update-licence",methods=['POST'])
def updateLicence():
    pass

@licenceBP.route("/search-tenants",methods=['POST'])
def searchTenants():
    pass

@licenceBP.route('/generate-new-licence', methods=['POST'])
def genrateNewLicence():
    request_data = request.get_json()
    encrypted_data = encrypt_data(str(request_data))
    insert_sql("license_data", {"licenses":encrypted_data}) 
    return jsonify({'message': 'Request received'}), 200

@licenceBP.route('/get-license-data/<int:id>', methods=['GET'])
def getLicenceData(id):
    query = f"SELECT * FROM license_data WHERE ID = {id}"
    userData = execute_raw_query(query)
    if not userData:
        return jsonify({'error': 'User not found'}), 404
    decrypted_data =  decrypt_data(userData[0]["licenses"]) 
    
    return jsonify(decrypted_data)