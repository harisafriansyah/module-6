from flask import Blueprint, jsonify, request
from extensions import db
from models import Employee

employee_bp = Blueprint('employees', __name__)
# POST /employees: Add a new employee to the zoo
@employee_bp.route('/employees', methods=['POST'])
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
@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.serialize() for employee in employees]), 200

# GET /employees/<id>: Retrieve a specific employee by their id
@employee_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = db.session.get(Employee, id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(employee.serialize()), 200

# PUT /employees/<id>: Update an existing employee by their id
@employee_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = db.session.get(Employee, id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    data = request.get_json()
    employee.name = data['name']
    employee.email = data['email']
    employee.phone_number = data.get('phone_number', employee.phone_number)
    employee.role = data.get('role', employee.role)
    employee.schedule = data.get('schedule', employee.schedule)

    db.session.commit()
    return jsonify(employee.serialize()), 200

# DELETE /employees/<id>: Delete an existing employee by their id
@employee_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = db.session.get(Employee, id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'}), 200