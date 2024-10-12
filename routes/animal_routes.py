from flask import Blueprint, jsonify, request
from extensions import db
from models import Animal

animal_bp = Blueprint('animals', __name__)
# POST /animals: Add a new animal to the zoo
@animal_bp.route('/animals', methods=['POST'])
def add_animal():
    data = request.get_json()
    new_animal = Animal(
        species=data['species'],
        age=data['age'],
        gender=data['gender'],
        special_requirements=data.get('special_requirements', '')
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'id': new_animal.id}), 201

# GET /animals: Retrieve a list of all animals in the zoo
@animal_bp.route('/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    return jsonify([{
        'id': animal.id,
        'species': animal.species,
        'age': animal.age,
        'gender': animal.gender,
        'special_requirements': animal.special_requirements
    } for animal in animals]), 200

# GET /animals/<id>: Retrieve a specific animal by its id
@animal_bp.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    animal = db.session.get(Animal, id)
    if animal is None:
        return jsonify({'error': 'Animal not found'}), 404
    
    return jsonify({
        'id': animal.id,
        'species': animal.species,
        'age': animal.age,
        'gender': animal.gender,
        'special_requirements': animal.special_requirements
    }), 200

# PUT /animals/<id>: Update an existing animal by its id
@animal_bp.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    animal = db.session.get(Animal, id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404

    data = request.get_json()
    animal.species = data['species']
    animal.age = data['age']
    animal.gender = data['gender']
    animal.special_requirements = data.get('special_requirements', '')

    db.session.commit()
    return jsonify({
        'id': animal.id,
        'species': animal.species,
        'age': animal.age,
        'gender': animal.gender,
        'special_requirements': animal.special_requirements
    }), 200

# DELETE /animals/<id>: Delete an existing animal by its id
@animal_bp.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = db.session.get(Animal, id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal deleted'}), 200