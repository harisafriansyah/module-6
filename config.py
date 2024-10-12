import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Create the SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DBUSERNAME')}:{os.getenv('DBPASSWORD')}"
        f"@{os.getenv('HOSTNAME')}:{os.getenv('DBPORT')}/{os.getenv('DATABASNAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False