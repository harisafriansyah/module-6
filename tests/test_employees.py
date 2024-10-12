def test_post_employee(client):
    # Test POST request to add a new employee
    response = client.post('/employees', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone_number': '123456789',
        'role': 'Zookeeper',
        'schedule': 'Mon-Fri'
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_get_employees(client):
    # Test GET request for all employees
    response = client.get('/employees')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_employee_by_id(client):
    # Add an employee first
    post_response = client.post('/employees', json={
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone_number': '987654321',
        'role': 'Veterinarian',
        'schedule': 'Mon-Wed'
    })
    employee_id = post_response.json['id']

    # Test GET request to retrieve the employee by ID
    get_response = client.get(f'/employees/{employee_id}')
    assert get_response.status_code == 200
    assert get_response.json['name'] == 'Jane Doe'

def test_update_employee(client):
    # Add an employee first
    post_response = client.post('/employees', json={
        'name': 'Alex Smith',
        'email': 'alex.smith@example.com',
        'phone_number': '1122334455',
        'role': 'Caretaker',
        'schedule': 'Tue-Sat'
    })
    employee_id = post_response.json['id']

    # Test PUT request to update employee details
    update_response = client.put(f'/employees/{employee_id}', json={
        'name': 'Alex Smith',
        'email': 'alex.smith@example.com',
        'phone_number': '1122334455',
        'role': 'Head Caretaker',
        'schedule': 'Mon-Fri'
    })
    assert update_response.status_code == 200
    assert update_response.json['role'] == 'Head Caretaker'

def test_delete_employee(client):
    # Add an employee first
    post_response = client.post('/employees', json={
        'name': 'George White',
        'email': 'george.white@example.com',
        'phone_number': '4455667788',
        'role': 'Guide',
        'schedule': 'Mon-Fri'
    })
    employee_id = post_response.json['id']

    # Test DELETE request to remove the employee
    delete_response = client.delete(f'/employees/{employee_id}')
    assert delete_response.status_code == 200

    # Confirm the employee is deleted by trying to GET it
    get_response = client.get(f'/employees/{employee_id}')
    assert get_response.status_code == 404
