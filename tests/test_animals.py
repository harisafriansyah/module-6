import pytest
from app import create_app
from models import Animal
from extensions import db

@pytest.fixture
def init_database(app):
    """Initialize the database with test data."""
    with app.app_context():
        # Add a sample animal for the tests
        animal = Animal(species="Tiger", age=5, gender="Male", special_requirements="Carnivore")
        db.session.add(animal)
        db.session.commit()

def test_get_animals(client, init_database):
    # Test if GET request to '/animals' returns status code 200
    response = client.get('/animals')

    # Debug: Print the status code and response data for inspection
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json}")

    assert response.status_code == 200

    # Ensure that the animals list contains the expected number of items
    assert len(response.json) == 2

def test_post_animal(client, init_database):
    # Test if POST request to '/animals' successfully adds a new animal
    response = client.post('/animals', json={
        'species': 'Lion',
        'age': 5,
        'gender': 'Male',
        'special_requirements': 'Large enclosure'
    })
    assert response.status_code == 201
    assert 'id' in response.json

    # Test if we can retrieve both animals (Tiger and Lion)
    get_response = client.get('/animals')
    assert get_response.status_code == 200
    assert len(get_response.json) == 2  # Tiger and Lion

def test_get_animal_by_id(client, init_database):
    # First, add an animal
    post_response = client.post('/animals', json={
        'species': 'Elephant',
        'age': 10,
        'gender': 'Female',
        'special_requirements': 'Water nearby'
    })
    assert post_response.status_code == 201

    animal_id = post_response.json['id']
    print(f'Animal ID after POST: {animal_id}')

    # Test GET request for the specific animal
    get_response = client.get(f'/animals/{animal_id}')
    print(f'GET response status code: {get_response.status_code}') 
    assert get_response.status_code == 200
    assert get_response.json['species'] == 'Elephant'

def test_update_animal(client, init_database):
    # Add an animal first
    post_response = client.post('/animals', json={
        'species': 'Giraffe',
        'age': 7,
        'gender': 'Female',
        'special_requirements': 'Tall trees'
    })
    animal_id = post_response.json['id']

    # Test PUT request to update the animal's details
    update_response = client.put(f'/animals/{animal_id}', json={
        'species': 'Giraffe',
        'age': 8,
        'gender': 'Female',
        'special_requirements': 'More tall trees'
    })
    assert update_response.status_code == 200
    assert update_response.json['age'] == 8

def test_delete_animal(client, init_database):
    # Add an animal first
    post_response = client.post('/animals', json={
        'species': 'Penguin',
        'age': 3,
        'gender': 'Male',
        'special_requirements': 'Cold environment'
    })
    animal_id = post_response.json['id']

    # Test DELETE request to remove the animal
    delete_response = client.delete(f'/animals/{animal_id}')
    assert delete_response.status_code == 200

    # Confirm the animal is deleted by trying to GET it
    get_response = client.get(f'/animals/{animal_id}')
    assert get_response.status_code == 404
