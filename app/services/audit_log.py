from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse
from app.utils.permission_checker import require_admin

# Helper function to create an audit log entry
def create_audit_log(db: Session, user_id: int, action: str, details: str) -> AuditLog:
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            timestamp=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating audit log: {str(e)}")

# Admin: Get all audit logs
def get_all_audit_logs(db: Session, current_user) -> List[AuditLogResponse]:
    require_admin(current_user)

    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit logs found")
    return logs

# Admin: Get audit logs by user
def get_audit_logs_by_user(db: Session, user_id: int, current_user) -> List[AuditLogResponse]:
    require_admin(current_user)

    logs = db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.timestamp.desc()).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit logs found for the specified user")
    return logs

# Admin: Get audit logs by action type
def get_audit_logs_by_action(db: Session, action: str, current_user) -> List[AuditLogResponse]:
    require_admin(current_user)

    logs = db.query(AuditLog).filter(AuditLog.action == action).order_by(AuditLog.timestamp.desc()).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit logs found for the specified action")
    return logs

# Admin: Get audit logs by date range
def get_audit_logs_by_date(db: Session, start_date: datetime, end_date: datetime, current_user) -> List[AuditLogResponse]:
    require_admin(current_user)

    logs = db.query(AuditLog).filter(
        AuditLog.timestamp >= start_date,
        AuditLog.timestamp <= end_date
    ).order_by(AuditLog.timestamp.desc()).all()

    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audit logs found in the specified date range")
    return logs

# Admin: Clear all audit logs (for maintenance)
def clear_audit_logs(db: Session, current_user) -> dict:
    require_admin(current_user)

    try:
        num_deleted = db.query(AuditLog).delete()
        db.commit()
        return {"message": f"All audit logs cleared, total deleted: {num_deleted}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error clearing audit logs: {str(e)}")
