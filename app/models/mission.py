from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models import Base

# Enum for mission status
class MissionStatus(PyEnum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    route_map_url = Column(String(255), nullable=True)  # Optional route map URL (e.g., Google Maps link)
    status = Column(Enum(MissionStatus), default=MissionStatus.PLANNED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    distance = Column(Float, nullable=True)  # Total distance of the mission
    total_load = Column(Float, nullable=True)  # Total load to be carried in the mission

    # Relationships
    driver = relationship("User", back_populates="missions")  # Link to the assigned driver
    vehicle = relationship("Vehicle", back_populates="missions")  # Link to the vehicle used
    orders = relationship("Order", back_populates="mission", cascade="all, delete-orphan")  # Orders grouped in the mission
    assignment_logs = relationship("MissionAssignmentLog", back_populates="mission", cascade="all, delete-orphan")  # Log of mission assignments
    routes = relationship("Route", back_populates="mission", cascade="all, delete-orphan")  # Optimized route for the mission

    def __repr__(self):
        return (f"<Mission(id={self.id}, driver_id={self.driver_id}, vehicle_id={self.vehicle_id}, "
                f"status='{self.status.name}', distance={self.distance}, total_load={self.total_load})>")
