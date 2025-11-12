from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ParkingSpace(db.Model):
    __tablename__ = "parking_spaces"
    id = db.Column(db.BigInteger, primary_key=True)
    owner_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)            # e.g., "Mall Parking A"
    address = db.Column(db.String(512))                          # human-friendly address
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    google_map_url = db.Column(db.String(1024), nullable=True)
    price_per_hour = db.Column(db.Numeric(8,2), default=0)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", backref="parking_spaces")

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)  # who booked
    parking_id = db.Column(db.BigInteger, db.ForeignKey("parking_spaces.id"), nullable=False)
    # Optional timed booking window. When either is NULL, treat booking as an indefinite exclusive lock
    # that makes the space unavailable to anyone else until removed/cancelled.
    time_start = db.Column(db.DateTime, nullable=True)
    time_end = db.Column(db.DateTime, nullable=True)
    # Optional duration in hours for convenience (derived from time_end-time_start if both provided)
    duration_hours = db.Column(db.Numeric(6,2), nullable=True)
    total_amount = db.Column(db.Numeric(10,2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="bookings")
    parking = db.relationship("ParkingSpace", backref="bookings")
