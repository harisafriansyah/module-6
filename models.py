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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role,
            'schedule': self.schedule
        }

class FeedingSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    enclosure_id = db.Column(db.Integer, nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    feeding_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Establish a relationship with the Animal model
    animal = db.relationship('Animal', backref=db.backref('feeding_schedules', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'enclosure_id': self.enclosure_id,
            'food_type': self.food_type,
            'feeding_time': self.feeding_time.isoformat()  # Convert datetime to ISO format
        }