import pytest
from models import FeedingSchedule, Animal
from datetime import datetime
from extensions import db

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Add an animal to associate with feeding schedules
        animal = Animal(species="Tiger", age=5, gender="Male", special_requirements="Carnivore")
        db.session.add(animal)
        db.session.commit()

@pytest.mark.usefixtures("init_database")
def test_add_feeding(client):
    # Get the animal ID to associate with the feeding schedule
    animal = Animal.query.first()
    assert animal is not None, "No animal found in the database!"

    # Test POST request to add a new feeding schedule
    response = client.post('/feedings', json={
        'animal_id': animal.id,
        'enclosure_id': 1,
        'food_type': 'Meat',
        'feeding_time': datetime.now().isoformat()
    })
    assert response.status_code == 201
    assert 'id' in response.json

@pytest.mark.usefixtures("init_database")
def test_get_feedings(client):
    # Test GET request to retrieve all feeding schedules
    response = client.get('/feedings')
    assert response.status_code == 200
    assert isinstance(response.json, list)

@pytest.mark.usefixtures("init_database")
def test_get_feeding_by_id(client):
    # First, add a feeding
    animal = Animal.query.first()
    assert animal is not None, "No animal found in the database!"

    post_response = client.post('/feedings', json={
        'animal_id': animal.id,
        'enclosure_id': 1,
        'food_type': 'Meat',
        'feeding_time': datetime.now().isoformat()
    })
    assert post_response.status_code == 201
    feeding_id = post_response.json['id']

    get_response = client.get(f'/feedings/{feeding_id}')
    assert get_response.status_code == 200
    assert get_response.json['food_type'] == 'Meat'

@pytest.mark.usefixtures("init_database")
def test_update_feeding(client):
    animal = Animal.query.first()
    assert animal is not None, "No animal found in the database!"

    post_response = client.post('/feedings', json={
        'animal_id': animal.id,
        'enclosure_id': 1,
        'food_type': 'Meat',
        'feeding_time': datetime.now().isoformat()
    })
    assert post_response.status_code == 201
    feeding_id = post_response.json['id']

    # Test PUT request to update a feeding schedule
    put_response = client.put(f'/feedings/{feeding_id}', json={
        'animal_id': animal.id,
        'enclosure_id': 2,
        'food_type': 'Fish',
        'feeding_time': datetime.now().isoformat()
    })
    assert put_response.status_code == 200
    assert put_response.json['food_type'] == 'Fish'

@pytest.mark.usefixtures("init_database")
def test_delete_feeding(client):
    animal = Animal.query.first()
    assert animal is not None, "No animal found in the database!"

    post_response = client.post('/feedings', json={
        'animal_id': animal.id,
        'enclosure_id': 1,
        'food_type': 'Meat',
        'feeding_time': datetime.now().isoformat()
    })
    assert post_response.status_code == 201
    feeding_id = post_response.json['id']

    # Test DELETE request to delete the feeding schedule
    delete_response = client.delete(f'/feedings/{feeding_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Feeding schedule deleted'
