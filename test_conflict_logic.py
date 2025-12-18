
import unittest
from datetime import datetime
from app import app, db, Event, Resource, EventResourceAllocation
from utils.conflict_checker import is_resource_available

class TestConflictLogic(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_no_conflict(self):
        with app.app_context():
            r1 = Resource(name="Room A", type="room")
            db.session.add(r1)
            db.session.commit()
            
            # Create an event 10-11
            e1 = Event(title="E1", start_time=datetime(2023, 1, 1, 10, 0), end_time=datetime(2023, 1, 1, 11, 0))
            db.session.add(e1)
            db.session.commit()
            
            alloc = EventResourceAllocation(event_id=e1.id, resource_id=r1.id)
            db.session.add(alloc)
            db.session.commit()
            
            # Check availability for 11-12 (No overlap)
            avail, reason = is_resource_available(r1.id, datetime(2023, 1, 1, 11, 0), datetime(2023, 1, 1, 12, 0))
            self.assertTrue(avail)

    def test_exact_overlap(self):
        with app.app_context():
            r1 = Resource(name="Room A", type="room")
            db.session.add(r1)
            db.session.commit()
            
            e1 = Event(title="E1", start_time=datetime(2023, 1, 1, 10, 0), end_time=datetime(2023, 1, 1, 11, 0))
            db.session.add(e1)
            db.session.commit()
            
            alloc = EventResourceAllocation(event_id=e1.id, resource_id=r1.id)
            db.session.add(alloc)
            db.session.commit()
            
            # Check availability for 10-11 (Exact overlap)
            avail, reason = is_resource_available(r1.id, datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 11, 0))
            self.assertFalse(avail)
            self.assertIn("Conflict", reason)

    def test_partial_overlap(self):
        with app.app_context():
            r1 = Resource(name="Room A", type="room")
            db.session.add(r1)
            db.session.commit()
            
            e1 = Event(title="E1", start_time=datetime(2023, 1, 1, 10, 0), end_time=datetime(2023, 1, 1, 12, 0))
            db.session.add(e1)
            db.session.commit()
            
            alloc = EventResourceAllocation(event_id=e1.id, resource_id=r1.id)
            db.session.add(alloc)
            db.session.commit()
            
            # Check availability for 11-13 (Partial overlap)
            avail, reason = is_resource_available(r1.id, datetime(2023, 1, 1, 11, 0), datetime(2023, 1, 1, 13, 0))
            self.assertFalse(avail)

if __name__ == '__main__':
    unittest.main()
