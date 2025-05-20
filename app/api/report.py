from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.responses import FileResponse
from app.services.report import (
    generate_mission_report,
    generate_order_report,
    generate_vehicle_report,
    generate_audit_log_report,
    generate_notification_report,
    download_report
)
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

report_router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# Generate a mission report with optional filters
@report_router.get("/missions", status_code=status.HTTP_200_OK)
def get_mission_report(
    status: Optional[str] = None,
    driver_id: Optional[int] = None,
    moderator_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can generate mission reports")
    return generate_mission_report(db=db, status=status, driver_id=driver_id, moderator_id=moderator_id, start_date=start_date, end_date=end_date)

# Generate an order report with optional filters
@report_router.get("/orders", status_code=status.HTTP_200_OK)
def get_order_report(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    item_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can generate order reports")
    return generate_order_report(db=db, status=status, customer_id=customer_id, driver_id=driver_id, vehicle_id=vehicle_id, item_id=item_id, start_date=start_date, end_date=end_date)

# Generate a vehicle report with an optional status filter
@report_router.get("/vehicles", status_code=status.HTTP_200_OK)
def get_vehicle_report(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can generate vehicle reports")
    return generate_vehicle_report(db=db, status=status)

# Generate an audit log report with an optional date range
@report_router.get("/audit-logs", status_code=status.HTTP_200_OK)
def get_audit_log_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can generate audit log reports")
    return generate_audit_log_report(db=db, start_date=start_date, end_date=end_date)

# Generate a notification report with an optional read filter
@report_router.get("/notifications", status_code=status.HTTP_200_OK)
def get_notification_report(
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can generate notification reports")
    return generate_notification_report(db=db, is_read=is_read)

# Download a report by ID
@report_router.get("/download/{report_id}", response_class=FileResponse)
def download_report_file(report_id: int, db: Session = Depends(get_db)):
    try:
        return download_report(db=db, report_id=report_id)
    except HTTPException as e:
        raise e
