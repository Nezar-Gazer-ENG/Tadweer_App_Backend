from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.vehicle import (
    create_vehicle,
    update_vehicle,
    suspend_vehicle,
    reactivate_vehicle,
    get_vehicle,
    list_vehicles
)
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.utils.dependencies import get_db, get_current_user
from app.models.user import User, UserRole

vehicle_router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

# Create a new vehicle (Admin/Moderator)
@vehicle_router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_new_vehicle(vehicle_data: VehicleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can create vehicles")
    return create_vehicle(db=db, vehicle_data=vehicle_data, current_user=current_user)

# Update vehicle details (Admin/Moderator)
@vehicle_router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_existing_vehicle(vehicle_id: int, vehicle_data: VehicleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can update vehicles")
    return update_vehicle(db=db, vehicle_id=vehicle_id, vehicle_data=vehicle_data, current_user=current_user)

# Suspend a vehicle (Admin/Moderator)
@vehicle_router.patch("/{vehicle_id}/suspend", status_code=status.HTTP_200_OK)
def suspend_existing_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can suspend vehicles")
    return suspend_vehicle(db=db, vehicle_id=vehicle_id, current_user=current_user)

# Reactivate a suspended vehicle (Admin/Moderator)
@vehicle_router.patch("/{vehicle_id}/reactivate", status_code=status.HTTP_200_OK)
def reactivate_existing_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can reactivate vehicles")
    return reactivate_vehicle(db=db, vehicle_id=vehicle_id, current_user=current_user)

# Get details of a specific vehicle (Admin/Moderator)
@vehicle_router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_details(vehicle_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can view vehicle details")
    return get_vehicle(db=db, vehicle_id=vehicle_id, current_user=current_user)

# List all vehicles with optional filters (Admin/Moderator)
@vehicle_router.get("/", response_model=List[VehicleResponse])
def list_all_vehicles(is_active: Optional[bool] = None, vehicle_type: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins or moderators can view the vehicle list")
    return list_vehicles(db=db, is_active=is_active, vehicle_type=vehicle_type)
