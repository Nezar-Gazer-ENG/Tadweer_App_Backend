from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import datetime
from app.models.mission import Mission, MissionStatus
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.notification import Notification
from app.schemas.mission import MissionCreate, MissionUpdate, MissionResponse
from app.utils.permission_checker import require_admin, require_moderator

# Helper function to get a mission by ID
def get_mission_by_id(db: Session, mission_id: int) -> Mission:
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    return mission

# Admin/Moderator: Create a new mission
def create_mission(db: Session, mission_data: MissionCreate, current_user) -> Mission:
    require_moderator(current_user)

    new_mission = Mission(
        driver_id=mission_data.driver_id,
        vehicle_id=mission_data.vehicle_id,
        status=MissionStatus.PLANNED,
        created_at=datetime.utcnow(),
        route_map_url=mission_data.route_map_url,
        notes=mission_data.notes
    )
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)

    # Notify the driver
    notification = Notification(
        recipient_id=mission_data.driver_id,
        message=f"A new mission has been assigned to you by {current_user.username}.",
        type="MISSION_ASSIGNMENT",
        created_at=datetime.utcnow()
    )
    db.add(notification)
    db.commit()

    return new_mission

# Admin/Moderator: Update an existing mission
def update_mission(db: Session, mission_id: int, mission_data: MissionUpdate, current_user) -> Mission:
    require_moderator(current_user)

    mission = get_mission_by_id(db, mission_id)

    # Update fields if provided
    if mission_data.status:
        mission.status = mission_data.status
    if mission_data.route_map_url:
        mission.route_map_url = mission_data.route_map_url
    if mission_data.notes:
        mission.notes = mission_data.notes

    mission.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(mission)
    return mission

# Admin: Delete a mission
def delete_mission(db: Session, mission_id: int, current_user):
    require_admin(current_user)

    mission = get_mission_by_id(db, mission_id)
    db.delete(mission)
    db.commit()
    return {"message": "Mission deleted successfully"}

# Driver: Mark an order within a mission as done
def mark_order_as_done(db: Session, mission_id: int, order_id: int, driver_id: int):
    mission = get_mission_by_id(db, mission_id)

    # Check if the mission is assigned to the driver
    if mission.driver_id != driver_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to complete this mission")

    order = db.query(Order).filter(Order.id == order_id, Order.status == OrderStatus.ASSIGNED).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found or not assigned")

    # Mark the order as done
    order.status = OrderStatus.COMPLETED
    db.commit()

    # Check if all orders in the mission are done
    orders = db.query(Order).filter(Order.mission_id == mission_id).all()
    all_done = all(order.status == OrderStatus.COMPLETED for order in orders)

    if all_done:
        mission.status = MissionStatus.COMPLETED
        db.commit()

        # Notify the creator of the mission
        notification = Notification(
            recipient_id=mission.created_by,
            message=f"Mission {mission_id} has been completed by driver {driver_id}.",
            type="MISSION_COMPLETION",
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()

    return {"message": "Order marked as done"}

# Get all missions (Admin/Moderator)
def list_all_missions(db: Session, current_user) -> List[MissionResponse]:
    require_moderator(current_user)
    missions = db.query(Mission).all()
    return missions

# Get mission by ID (Admin/Moderator/Driver)
def get_mission(db: Session, mission_id: int, current_user) -> MissionResponse:
    mission = get_mission_by_id(db, mission_id)

    # Check access permission
    if current_user.role == "DRIVER" and mission.driver_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return mission
