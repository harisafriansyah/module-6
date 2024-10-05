import pytest
from app import create_app, db
from models import Animal

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all() 
        yield app
        db.session.remove()
        db.drop_all()  

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_get_animals(client):
    # Test if GET request to '/animals' returns status code 200
    response = client.get('/animals')
    assert response.status_code == 200
    assert response.json == []  

def test_post_animal(client):
    # Test if POST request to '/animals' successfully adds a new animal
    response = client.post('/animals', json={
        'species': 'Lion',
        'age': 5,
        'gender': 'Male',
        'special_requirements': 'Large enclosure'
    })
    assert response.status_code == 201
    assert 'id' in response.json

    # Test if we can retrieve the posted animal
    get_response = client.get('/animals')
    assert get_response.status_code == 200
    assert len(get_response.json) == 1
    assert get_response.json[0]['species'] == 'Lion'

def test_get_animal_by_id(client):
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
