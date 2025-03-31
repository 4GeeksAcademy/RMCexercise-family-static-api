import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "id": 1,
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "id": 2,
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "id": 3,
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
})

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({
            "first_name": None,
            "last_name": None,
            "age": None,
            "lucky_numbers": None,
            "id": None,
            "error": "No existe"
        }), 200
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def create_member():
    if not request.is_json:
        return jsonify({"error": "El request debe ser JSON"}), 400

    member = request.get_json()

    required_fields = ["first_name", "id", "age", "lucky_numbers"]
    if not all(field in member for field in required_fields):
        return jsonify({"error": "Campos requeridos: first_name, id, age, lucky_numbers"}), 400

    if jackson_family.get_member(member["id"]):
        return jsonify({"error": "ID ya existe"}), 400

    jackson_family.add_member(member)
    return jsonify({"message": "Miembro agregado", "familiar": member}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    jackson_family.delete_member(id) 
    return jsonify({"message": f"El familiar con ID {id} fue eliminado", "done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
