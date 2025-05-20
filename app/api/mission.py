from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.mission import (
    create_mission,
    update_mission,
    delete_mission,
    mark_order_as_done,
    list_all_missions,
    get_mission
)
from app.schemas.mission import MissionCreate, MissionUpdate, MissionResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

mission_router = APIRouter(
    prefix="/missions",
    tags=["Missions"]
)

# Create a new mission (Admin/Moderator)
@mission_router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_new_mission(mission_data: MissionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can create missions")
    return create_mission(db=db, mission_data=mission_data, current_user=current_user)

# Update an existing mission (Admin/Moderator)
@mission_router.put("/{mission_id}", response_model=MissionResponse)
def update_existing_mission(mission_id: int, mission_data: MissionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can update missions")
    return update_mission(db=db, mission_id=mission_id, mission_data=mission_data, current_user=current_user)

# Delete a mission (Admin only)
@mission_router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_mission(mission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete missions")
    return delete_mission(db=db, mission_id=mission_id, current_user=current_user)

# Mark an order as done within a mission (Driver)
@mission_router.post("/{mission_id}/orders/{order_id}/done", status_code=status.HTTP_200_OK)
def mark_order_complete(mission_id: int, order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.DRIVER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can mark orders as done")
    return mark_order_as_done(db=db, mission_id=mission_id, order_id=order_id, driver_id=current_user.id)

# List all missions (Admin/Moderator)
@mission_router.get("/", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can view all missions")
    return list_all_missions(db=db, current_user=current_user)

# Get a specific mission by ID (Admin/Moderator/Driver)
@mission_router.get("/{mission_id}", response_model=MissionResponse)
def get_mission_details(mission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_mission(db=db, mission_id=mission_id, current_user=current_user)
