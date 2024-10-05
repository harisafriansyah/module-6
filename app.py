from flask import Flask
from extensions import db 
from models import Animal, Employee, FeedingSchedule
from routes import api 
from flask_migrate import Migrate

migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize the database with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Connect migrations with the app and db

    # Register the blueprint for routes
    app.register_blueprint(api, url_prefix='/')

    # Ensure that everything is connected in the app context
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

# Run the Flask app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
