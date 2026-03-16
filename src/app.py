"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all():
    members = jackson_family.get_all_members()
    
    # response = {
    #         "hello": "world",
    #     "family": members} #Si se utiliza el response para dar formato a la salida no pasa el test
    
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_get_member(id):
    member = jackson_family.get_member(id)
    
    if member:
        # response = {"family": member} Si se utiliza el response para dar formato a la salida no pasa el test
        return  jsonify(member), 200
    
    return jsonify({'mensaje': "Miembro familiar no encontrado"}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def handle_update_member(id):
    body = request.get_json()
    
    if not body:
        return jsonify({"mensaje": "El body está vacío"}), 400
    
    actualizado = jackson_family.update_member(id, body)
    
    if actualizado:
        return jsonify({'mensaje': "Miembro familiar actualizado", "member": actualizado}), 200
    else:
        return jsonify({'mensaje': 'Miembro familiar no encontrado'}), 404
    

@app.route('/members', methods=['POST'])
def hande_add_member():
    body = request.get_json()
    
    if not body:
        return jsonify({"mensaje": "El body está vacío"}), 400
    
    nuevo_miembro = jackson_family.add_member(body)
    # response = {"family": nuevo_miembro} Si se utiliza el response para dar formato a la salida no pasa el test
    return jsonify(nuevo_miembro), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    resultado = jackson_family.delete_member(id)
    
    if resultado:
        return jsonify({"done": True}), 200
    
    return jsonify({"mensaje": 'Miembro familiar no encontrado'}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
