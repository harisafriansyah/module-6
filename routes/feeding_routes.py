from flask import Blueprint, jsonify, request
from extensions import db
from models import FeedingSchedule
from datetime import datetime

feeding_bp = Blueprint('feedings', __name__)

# GET /feedings: Retrieve all feeding schedules
@feeding_bp.route('/feedings', methods=['GET'])
def get_feedings():
    feedings = FeedingSchedule.query.all()
    return jsonify([feeding.serialize() for feeding in feedings]), 200

# GET /feedings/<int:id>: Retrieve a specific feeding schedule by id
@feeding_bp.route('/feedings/<int:id>', methods=['GET'])
def get_feeding_by_id(id):
    feeding = db.session.get(FeedingSchedule, id)  # Updated to use Session.get()
    if not feeding:
        return jsonify({'error': 'Feeding not found'}), 404
    return jsonify(feeding.serialize()), 200

# POST /feedings: Add a new feeding schedule
@feeding_bp.route('/feedings', methods=['POST'])
def add_feeding():
    data = request.get_json()
    new_feeding = FeedingSchedule(
        animal_id=data['animal_id'],
        enclosure_id=data['enclosure_id'],
        food_type=data['food_type'],
        feeding_time=datetime.fromisoformat(data['feeding_time'])
    )
    db.session.add(new_feeding)
    db.session.commit()
    return jsonify(new_feeding.serialize()), 201

# PUT /feedings/<int:id>: Update an existing feeding schedule
@feeding_bp.route('/feedings/<int:id>', methods=['PUT'])
def update_feeding(id):
    feeding = db.session.get(FeedingSchedule, id)
    if not feeding:
        return jsonify({'error': 'Feeding not found'}), 404
    data = request.get_json()
    feeding.animal_id = data['animal_id']
    feeding.enclosure_id = data['enclosure_id']
    feeding.food_type = data['food_type']
    feeding.feeding_time = datetime.fromisoformat(data['feeding_time'])
    
    db.session.commit()
    return jsonify(feeding.serialize()), 200

# DELETE /feedings/<int:id>: Delete a feeding schedule by id
@feeding_bp.route('/feedings/<int:id>', methods=['DELETE'])
def delete_feeding(id):
    feeding = db.session.get(FeedingSchedule, id)
    if not feeding:
        return jsonify({'error': 'Feeding not found'}), 404
    db.session.delete(feeding)
    db.session.commit()
    return jsonify({'message': 'Feeding schedule deleted'}), 200