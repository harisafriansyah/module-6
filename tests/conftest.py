import pytest
from app import create_app, db
from models import Animal

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory SQLite for testing
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()  # Clean up the session
        db.drop_all()  # Teardown the database

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        animal = Animal(species="Tiger", age=5, gender="Male", special_requirements="Carnivore")
        db.session.add(animal)
        db.session.commit()
        yield db
        db.drop_all()
