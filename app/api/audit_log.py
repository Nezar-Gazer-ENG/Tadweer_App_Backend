from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.services.audit_log import (
    create_audit_log,
    get_all_audit_logs,
    get_audit_logs_by_user,
    get_audit_logs_by_action,
    get_audit_logs_by_date,
    clear_audit_logs
)
from app.schemas.audit_log import AuditLogResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

audit_log_router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

# Create a new audit log entry (Internal Use)
@audit_log_router.post("/", status_code=status.HTTP_201_CREATED)
def log_action(user_id: int, action: str, details: str, db: Session = Depends(get_db)):
    return create_audit_log(db=db, user_id=user_id, action=action, details=details)

# Get all audit logs (Admin only)
@audit_log_router.get("/", response_model=List[AuditLogResponse])
def list_all_audit_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view audit logs")
    return get_all_audit_logs(db=db, current_user=current_user)

# Get audit logs by user ID (Admin only)
@audit_log_router.get("/user/{user_id}", response_model=List[AuditLogResponse])
def get_logs_by_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view user-specific audit logs")
    return get_audit_logs_by_user(db=db, user_id=user_id, current_user=current_user)

# Get audit logs by action type (Admin only)
@audit_log_router.get("/action/{action}", response_model=List[AuditLogResponse])
def get_logs_by_action(action: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view action-specific audit logs")
    return get_audit_logs_by_action(db=db, action=action, current_user=current_user)

# Get audit logs by date range (Admin only)
@audit_log_router.get("/date-range", response_model=List[AuditLogResponse])
def get_logs_by_date(start_date: datetime, end_date: datetime, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view date-specific audit logs")
    return get_audit_logs_by_date(db=db, start_date=start_date, end_date=end_date, current_user=current_user)

# Clear all audit logs (Admin only)
@audit_log_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_audit_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can clear audit logs")
    return clear_audit_logs(db=db, current_user=current_user)
