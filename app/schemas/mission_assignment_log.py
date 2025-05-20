from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum for assignment status
class AssignmentStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

# Schema for creating a mission assignment log entry
class MissionAssignmentCreate(BaseModel):
    mission_id: int = Field(..., example=1)
    driver_id: int = Field(..., example=2)
    status: AssignmentStatus = Field(..., example="ASSIGNED")
    remarks: Optional[str] = Field(None, example="Assigned after route optimization")

# Schema for updating an existing mission assignment log entry
class MissionAssignmentUpdate(BaseModel):
    status: Optional[AssignmentStatus] = Field(None, example="COMPLETED")
    remarks: Optional[str] = Field(None, example="Driver reported successful delivery")

# Schema for returning mission assignment log details
class MissionAssignmentResponse(BaseModel):
    id: int
    mission_id: int
    driver_id: int
    status: AssignmentStatus
    timestamp: datetime
    remarks: Optional[str]

    class Config:
        from_attributes = True

# Schema for deleting a mission assignment log entry
class MissionAssignmentDelete(BaseModel):
    id: int
    message: str = Field(default="Mission assignment log deleted successfully.")
