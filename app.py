from flask import Flask
from flask_migrate import Migrate
from extensions import db
from routes.animal_routes import animal_bp
from routes.employee_routes import employee_bp
from routes.feeding_routes import feeding_bp
from routes.report_routes import report_bp
from dotenv import load_dotenv
import os

def create_app(config_class='config.Config'):
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()

    # Load the configuration from the provided config class
    app.config.from_object(config_class)

    # Initialize database with app
    db.init_app(app)

    # Initialize Flask-Migrate for database migrations
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(animal_bp, url_prefix='/')
    app.register_blueprint(employee_bp, url_prefix='/')
    app.register_blueprint(feeding_bp, url_prefix='/')
    app.register_blueprint(report_bp, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
