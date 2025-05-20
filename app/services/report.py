from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
from app.models.order_item import OrderItem
from app.models import Mission, Order, Vehicle, AuditLog, Notification
from app.utils.pdf_generator import generate_pdf
from app.utils.file_handler import save_file
from datetime import datetime
from typing import Optional, List

# Helper to parse date strings or None
def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if date_str:
        return datetime.fromisoformat(date_str)
    return None

# Missions report with optional filters
def generate_mission_report(
    db: Session,
    status: Optional[str] = None,
    driver_id: Optional[int] = None,
    moderator_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    query = db.query(Mission)
    if status:
        query = query.filter(Mission.status == status)
    if driver_id:
        query = query.filter(Mission.driver_id == driver_id)
    if moderator_id:
        query = query.filter(Mission.created_by_moderator == moderator_id)
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        query = query.filter(Mission.created_at.between(start, end))
    missions = query.all()
    if not missions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No missions found")

    data = [{
        "Mission ID": m.mission_id,
        "Status": m.status,
        "Driver ID": m.driver_id,
        "Moderator ID": m.created_by_moderator,
        "Vehicle ID": m.vehicle_id,
        "Created At": m.created_at,
    } for m in missions]

    pdf_path = generate_pdf(data, "Mission Report")
    return {"report_id": 1, "path": pdf_path, "status": "Ready"}

# Orders report with flexible filters
def generate_order_report(
    db: Session,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    item_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    if driver_id:
        query = query.filter(Order.driver_id == driver_id)
    if vehicle_id:
        query = query.filter(Order.vehicle_id == vehicle_id)
    if item_id:
        query = query.join(Order.items).filter(OrderItem.item_id == item_id)
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        query = query.filter(Order.created_at.between(start, end))

    orders = query.all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found")

    data = [{
        "Order ID": o.order_id,
        "Status": o.status,
        "Customer ID": o.customer_id,
        "Driver ID": o.driver_id,
        "Vehicle ID": o.vehicle_id,
        "Created At": o.created_at,
    } for o in orders]

    pdf_path = generate_pdf(data, "Order Report")
    return {"report_id": 2, "path": pdf_path, "status": "Ready"}

# Vehicle report (optional status filter)
def generate_vehicle_report(db: Session, status: Optional[str] = None):
    query = db.query(Vehicle)
    if status:
        query = query.filter(Vehicle.status == status)
    vehicles = query.all()
    if not vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vehicles found")

    data = [{
        "Vehicle ID": v.vehicle_id,
        "Name": v.name,
        "Capacity": v.capacity,
        "Status": v.status,
        "Created At": v.created_at,
    } for v in vehicles]

    pdf_path = generate_pdf(data, "Vehicle Report")
    return {"report_id": 3, "path": pdf_path, "status": "Ready"}

# Audit log report with optional date range
def generate_audit_log_report(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None):
    query = db.query(AuditLog)
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        query = query.filter(AuditLog.timestamp.between(start, end))
    logs = query.all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit logs found")

    data = [{
        "Action": l.action,
        "Initiator": l.initiator_id,
        "Role": l.initiator_role,
        "Details": l.details,
        "Timestamp": l.timestamp,
    } for l in logs]

    pdf_path = generate_pdf(data, "Audit Log Report")
    return {"report_id": 4, "path": pdf_path, "status": "Ready"}

# Notification report with optional read filter
def generate_notification_report(db: Session, is_read: Optional[bool] = None):
    query = db.query(Notification)
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    notifications = query.all()
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")

    data = [{
        "Notification ID": n.notification_id,
        "Message": n.message,
        "Recipient": n.recipient_id,
        "Status": "Read" if n.is_read else "Unread",
        "Created At": n.created_at,
    } for n in notifications]

    pdf_path = generate_pdf(data, "Notification Report")
    return {"report_id": 5, "path": pdf_path, "status": "Ready"}

# Download a report file by ID
def download_report(db: Session, report_id: int):
    report_path = f"/mnt/data/reports/report_{report_id}.pdf"
    try:
        file = save_file(report_path)
        return file
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
