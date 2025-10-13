# seed_data.py
from app import create_app
from app.models import db, User, ParkingSpace
from werkzeug.security import generate_password_hash
from decimal import Decimal

app = create_app()
with app.app_context():
    # create demo user if not exists
    user = User.query.filter_by(username='demo_owner').first()
    if not user:
        user = User(username='demo_owner', email='owner@example.com', password_hash=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()

    # add parking spaces if none exist
    if ParkingSpace.query.count() == 0:
        slots = [
            {"owner_id": user.id, "title":"Mall Parking A", "address":"Mall Road", "lat":12.9716, "lng":77.5946, "price_per_hour": Decimal('30.00')},
            {"owner_id": user.id, "title":"Office Tower B", "address":"Business Park", "lat":12.9728, "lng":77.5950, "price_per_hour": Decimal('60.00')},
            {"owner_id": user.id, "title":"Market Square", "address":"Market St", "lat":12.9700, "lng":77.5900, "price_per_hour": Decimal('20.00')},
        ]
        for s in slots:
            ps = ParkingSpace(**s)
            db.session.add(ps)
        db.session.commit()
        print("Seeded parking slots.")
    else:
        print("Parking slots already exist.")
