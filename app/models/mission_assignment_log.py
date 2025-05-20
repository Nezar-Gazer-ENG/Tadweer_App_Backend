from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models import Base

# Enum for assignment log status
class AssignmentStatus(PyEnum):
    ASSIGNED = "ASSIGNED"
    UPDATED = "UPDATED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class MissionAssignmentLog(Base):
    __tablename__ = "mission_assignment_logs"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.ASSIGNED, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the assignment or update occurred
    remarks = Column(Text, nullable=True)  # Optional comments or reasons for the change

    # Relationships
    mission = relationship("Mission", back_populates="assignment_logs")  # Link to the mission being logged
    driver = relationship("User", back_populates="assignment_logs")  # Link to the driver involved in the assignment

    def __repr__(self):
        return (f"<MissionAssignmentLog(id={self.id}, mission_id={self.mission_id}, driver_id={self.driver_id}, "
                f"status='{self.status.name}', timestamp={self.timestamp})>")
