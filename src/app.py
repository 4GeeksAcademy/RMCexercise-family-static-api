import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    members = [member for member in members] 
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        member = {
            "name": member["first_name"] + " " + member["last_name"],
            "id": id,
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
    if member is None:
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
    member = request.json
    member["id"] = jackson_family._generate_id()  # Assuming _generate_id exists in FamilyStructure
    jackson_family.add_member(member)
    return jsonify({"message": "Agregado", "familiar": member}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)
    jackson_family.delete_member(id)
    return jsonify({"message": f"El familiar con el id {id} fue eliminado", "done": True}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
