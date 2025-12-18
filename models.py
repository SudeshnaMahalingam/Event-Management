from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationship to allocations
    allocations = db.relationship('EventResourceAllocation', backref='event', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event {self.title}>'

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # 'room', 'instructor', 'equipment'

    # Relationship to allocations
    allocations = db.relationship('EventResourceAllocation', backref='resource', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Resource {self.name} ({self.type})>'

class EventResourceAllocation(db.Model):
    __tablename__ = 'event_resource_allocation'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

    def __repr__(self):
        return f'<Allocation Event:{self.event_id} Resource:{self.resource_id}>'
