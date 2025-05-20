from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.models.mission_assignment_log import MissionAssignmentLog
from app.schemas.mission_assignment_log import (
    MissionAssignmentCreate,
    MissionAssignmentUpdate,
    MissionAssignmentResponse,
    MissionAssignmentDelete
)
from app.utils.permission_checker import require_admin

# Helper function to create a mission assignment log entry
def create_assignment_log(db: Session, log_data: MissionAssignmentCreate, assigned_by: int) -> MissionAssignmentLog:
    try:
        assignment_log = MissionAssignmentLog(
            mission_id=log_data.mission_id,
            driver_id=log_data.driver_id,
            status=log_data.status,
            remarks=log_data.remarks,
            timestamp=datetime.utcnow(),
            assigned_by=assigned_by
        )
        db.add(assignment_log)
        db.commit()
        db.refresh(assignment_log)
        return assignment_log
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating assignment log: {str(e)}")

# Admin: Get all mission assignment logs
def get_all_assignment_logs(db: Session, current_user) -> List[MissionAssignmentResponse]:
    require_admin(current_user)

    logs = db.query(MissionAssignmentLog).order_by(MissionAssignmentLog.timestamp.desc()).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No mission assignment logs found")
    return logs

# Admin: Get assignment logs by driver ID
def get_logs_by_driver(db: Session, driver_id: int, current_user) -> List[MissionAssignmentResponse]:
    require_admin(current_user)

    logs = db.query(MissionAssignmentLog).filter(MissionAssignmentLog.driver_id == driver_id).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assignment logs found for this driver")
    return logs

# Admin: Get assignment logs by mission ID
def get_logs_by_mission(db: Session, mission_id: int, current_user) -> List[MissionAssignmentResponse]:
    require_admin(current_user)

    logs = db.query(MissionAssignmentLog).filter(MissionAssignmentLog.mission_id == mission_id).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assignment logs found for this mission")
    return logs

# Admin: Get assignment logs by status
def get_logs_by_status(db: Session, status: str, current_user) -> List[MissionAssignmentResponse]:
    require_admin(current_user)

    logs = db.query(MissionAssignmentLog).filter(MissionAssignmentLog.status == status).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No assignment logs found with status {status}")
    return logs

# Admin: Update assignment log status or remarks
def update_assignment_log(db: Session, log_id: int, update_data: MissionAssignmentUpdate, current_user) -> MissionAssignmentLog:
    require_admin(current_user)

    assignment_log = db.query(MissionAssignmentLog).filter(MissionAssignmentLog.id == log_id).first()
    if not assignment_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment log not found")

    # Update fields if provided
    if update_data.status:
        assignment_log.status = update_data.status
    if update_data.remarks:
        assignment_log.remarks = update_data.remarks

    assignment_log.timestamp = datetime.utcnow()
    db.commit()
    db.refresh(assignment_log)
    return assignment_log

# Admin: Delete a mission assignment log
def delete_assignment_log(db: Session, log_id: int, current_user) -> MissionAssignmentDelete:
    require_admin(current_user)

    assignment_log = db.query(MissionAssignmentLog).filter(MissionAssignmentLog.id == log_id).first()
    if not assignment_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment log not found")

    db.delete(assignment_log)
    db.commit()
    return MissionAssignmentDelete(id=log_id)
