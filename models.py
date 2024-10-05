from extensions import db
from datetime import datetime

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    special_requirements = db.Column(db.String(200), nullable=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20))
    role = db.Column(db.String(50))
    schedule = db.Column(db.Text)

class FeedingSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    enclosure_id = db.Column(db.Integer, nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    feeding_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    animal = db.relationship('Animal', backref=db.backref('feeding_schedules', lazy=True))
