from flask import Blueprint, jsonify, request
from extensions import db
from models import Animal, Employee, FeedingSchedule
from datetime import datetime

api = Blueprint('api', __name__)

# Animal Management

# POST /animals: Add a new animal to the zoo
@api.route('/animals', methods=['POST'])
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
@api.route('/animals', methods=['GET'])
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
@api.route('/animals/<int:id>', methods=['GET'])
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
@api.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    animal = Animal.query.get_or_404(id)
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
@api.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal deleted'}), 200

# Employee Management

# POST /employees: Add a new employee to the zoo
@api.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        name=data['name'],
        email=data['email'],
        phone_number=data.get('phone_number'),
        role=data.get('role'),
        schedule=data.get('schedule')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id}), 201

# GET /employees: Retrieve a list of all employees in the zoo
@api.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.serialize() for employee in employees]), 200

# GET /employees/<id>: Retrieve a specific employee by their id
@api.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.serialize()), 200

# PUT /employees/<id>: Update an existing employee by their id
@api.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()

    employee.name = data['name']
    employee.email = data['email']
    employee.phone_number = data.get('phone_number', employee.phone_number)
    employee.role = data.get('role', employee.role)
    employee.schedule = data.get('schedule', employee.schedule)

    db.session.commit()
    return jsonify(employee.serialize()), 200

# DELETE /employees/<id>: Delete an existing employee by their id
@api.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'}), 200

#Feeding Schedules

# GET /feedings: Retrieve all feeding schedules
@api.route('/feedings', methods=['GET'])
def get_feedings():
    feedings = FeedingSchedule.query.all()
    return jsonify([feeding.serialize() for feeding in feedings]), 200

# GET /feedings/<int:id>: Retrieve a specific feeding schedule by id
@api.route('/feedings/<int:id>', methods=['GET'])
def get_feeding_by_id(id):
    feeding = FeedingSchedule.query.get_or_404(id)
    return jsonify(feeding.serialize()), 200

# POST /feedings: Add a new feeding schedule
@api.route('/feedings', methods=['POST'])
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
@api.route('/feedings/<int:id>', methods=['PUT'])
def update_feeding(id):
    feeding = FeedingSchedule.query.get_or_404(id)
    data = request.get_json()
    feeding.animal_id = data['animal_id']
    feeding.enclosure_id = data['enclosure_id']
    feeding.food_type = data['food_type']
    feeding.feeding_time = datetime.fromisoformat(data['feeding_time'])
    
    db.session.commit()
    return jsonify(feeding.serialize()), 200

# DELETE /feedings/<int:id>: Delete a feeding schedule by id
@api.route('/feedings/<int:id>', methods=['DELETE'])
def delete_feeding(id):
    feeding = FeedingSchedule.query.get_or_404(id)
    db.session.delete(feeding)
    db.session.commit()
    return jsonify({'message': 'Feeding schedule deleted'}), 200

# GET /reports/animals: Retrieve a report on the number and distribution of animals in the zoo
@api.route('/reports/animals', methods=['GET'])
def animal_report():
    from sqlalchemy import func

    report = db.session.query(
        Animal.species,
        Animal.gender,
        func.count(Animal.id).label('count')
    ).group_by(Animal.species, Animal.gender).all()

    result = [{'species': species, 'gender': gender, 'count': count} for species, gender, count in report]
    return jsonify(result), 200

# GET /reports/visitors: Retrieve a report on the number and behavior of visitors in the zoo
@api.route('/reports/visitors', methods=['GET'])
def visitor_report():
    report = [
        {'ticket_type': 'Adult', 'date': '2024-10-01', 'count': 200},
        {'ticket_type': 'Child', 'date': '2024-10-01', 'count': 50},
    ]
    return jsonify(report), 200

# GET /reports/revenue: Retrieve a report on the revenue generated by the zoo
@api.route('/reports/revenue', methods=['GET'])
def revenue_report():
    report = [
        {'ticket_type': 'Adult', 'event_type': 'General Admission', 'date': '2024-10-01', 'revenue': 2000},
        {'ticket_type': 'Child', 'event_type': 'General Admission', 'date': '2024-10-01', 'revenue': 500},
    ]
    return jsonify(report), 200
