from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.utils.permission_checker import require_admin, require_moderator

# Helper function to get a vehicle by ID
def get_vehicle_by_id(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle

# Admin/Moderator: Create a new vehicle
def create_vehicle(db: Session, vehicle_data: VehicleCreate, current_user) -> Vehicle:
    require_moderator(current_user)

    # Check for duplicate license plate
    existing_vehicle = db.query(Vehicle).filter(Vehicle.license_plate == vehicle_data.license_plate).first()
    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A vehicle with this license plate already exists."
        )

    new_vehicle = Vehicle(
        license_plate=vehicle_data.license_plate,
        vehicle_type=vehicle_data.vehicle_type,
        capacity=vehicle_data.capacity,
        is_active=True
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# Admin/Moderator: Update vehicle details
def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleUpdate, current_user) -> Vehicle:
    require_moderator(current_user)

    vehicle = get_vehicle_by_id(db, vehicle_id)

    # Update fields if provided
    if vehicle_data.license_plate:
        vehicle.license_plate = vehicle_data.license_plate
    if vehicle_data.vehicle_type:
        vehicle.vehicle_type = vehicle_data.vehicle_type
    if vehicle_data.capacity:
        vehicle.capacity = vehicle_data.capacity

    db.commit()
    db.refresh(vehicle)
    return vehicle

# Admin/Moderator: Suspend a vehicle (deactivate instead of delete)
def suspend_vehicle(db: Session, vehicle_id: int, current_user) -> dict:
    require_moderator(current_user)

    vehicle = get_vehicle_by_id(db, vehicle_id)
    if not vehicle.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle is already suspended")

    vehicle.is_active = False
    db.commit()
    return {"message": "Vehicle suspended successfully"}

# Admin/Moderator: Reactivate a suspended vehicle
def reactivate_vehicle(db: Session, vehicle_id: int, current_user) -> dict:
    require_moderator(current_user)

    vehicle = get_vehicle_by_id(db, vehicle_id)
    if vehicle.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle is already active")

    vehicle.is_active = True
    db.commit()
    return {"message": "Vehicle reactivated successfully"}

# Admin/Moderator: Get vehicle details
def get_vehicle(db: Session, vehicle_id: int, current_user) -> VehicleResponse:
    require_moderator(current_user)

    vehicle = get_vehicle_by_id(db, vehicle_id)
    return vehicle

# Admin/Moderator: List all vehicles with optional filter
def list_vehicles(db: Session, is_active: Optional[bool] = None, vehicle_type: Optional[str] = None) -> List[VehicleResponse]:
    query = db.query(Vehicle)

    if is_active is not None:
        query = query.filter(Vehicle.is_active == is_active)
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)

    vehicles = query.all()
    if not vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vehicles found")
    return vehicles
