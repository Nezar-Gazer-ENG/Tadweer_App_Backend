# test_create_tables.py
from app.database import engine, Base
from app.models.user import User
from app.models.order import Order
from app.models.vehicle import Vehicle
from app.models.address import Address
from app.models.order_item import OrderItem
from app.models.route import Route
from app.models.mission import Mission
from app.models.notification import Notification
from app.models.audit_log import AuditLog
from app.models.mission_assignment_log import MissionAssignmentLog
from app.models.item import Item

print("Creating tables directly...")
Base.metadata.create_all(bind=engine)
print("Tables created.")
