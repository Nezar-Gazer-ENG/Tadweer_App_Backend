from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.mission_assignment_log import (
    create_assignment_log,
    get_all_assignment_logs,
    get_logs_by_driver,
    get_logs_by_mission,
    get_logs_by_status,
    update_assignment_log,
    delete_assignment_log
)
from app.schemas.mission_assignment_log import (
    MissionAssignmentCreate,
    MissionAssignmentUpdate,
    MissionAssignmentResponse,
    MissionAssignmentDelete
)
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

mission_assignment_log_router = APIRouter(
    prefix="/mission-assignment-logs",
    tags=["Mission Assignment Logs"]
)

# Create a new mission assignment log (Admin only)
@mission_assignment_log_router.post("/", response_model=MissionAssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_new_assignment_log(log_data: MissionAssignmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create assignment logs")
    return create_assignment_log(db=db, log_data=log_data, assigned_by=current_user.id)

# Get all mission assignment logs (Admin only)
@mission_assignment_log_router.get("/", response_model=List[MissionAssignmentResponse])
def list_all_assignment_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view assignment logs")
    return get_all_assignment_logs(db=db, current_user=current_user)

# Get assignment logs by driver ID (Admin only)
@mission_assignment_log_router.get("/driver/{driver_id}", response_model=List[MissionAssignmentResponse])
def get_assignment_logs_by_driver(driver_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view driver assignment logs")
    return get_logs_by_driver(db=db, driver_id=driver_id, current_user=current_user)

# Get assignment logs by mission ID (Admin only)
@mission_assignment_log_router.get("/mission/{mission_id}", response_model=List[MissionAssignmentResponse])
def get_assignment_logs_by_mission(mission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view mission assignment logs")
    return get_logs_by_mission(db=db, mission_id=mission_id, current_user=current_user)

# Get assignment logs by status (Admin only)
@mission_assignment_log_router.get("/status/{status}", response_model=List[MissionAssignmentResponse])
def get_assignment_logs_by_status(status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view assignment logs by status")
    return get_logs_by_status(db=db, status=status, current_user=current_user)

# Update a mission assignment log (Admin only)
@mission_assignment_log_router.put("/{log_id}", response_model=MissionAssignmentResponse)
def update_existing_assignment_log(log_id: int, update_data: MissionAssignmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update assignment logs")
    return update_assignment_log(db=db, log_id=log_id, update_data=update_data, current_user=current_user)

# Delete a mission assignment log (Admin only)
@mission_assignment_log_router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment_log_entry(log_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete assignment logs")
    delete_assignment_log(db=db, log_id=log_id, current_user=current_user)
    return {"message": "Mission assignment log deleted successfully"}

