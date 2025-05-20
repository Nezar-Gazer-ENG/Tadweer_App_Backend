from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum for mission status
class MissionStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# Schema for creating a new mission
class MissionCreate(BaseModel):
    driver_id: int = Field(..., example=1)
    vehicle_id: int = Field(..., example=2)
    orders: List[int] = Field(..., example=[1, 2, 3])
    status: Optional[MissionStatus] = Field(default=MissionStatus.PLANNED, example="PLANNED")
    route_map_url: Optional[str] = Field(None, example="https://maps.google.com/route/123")
    notes: Optional[str] = Field(None, example="Prioritize large items")

# Schema for updating an existing mission
class MissionUpdate(BaseModel):
    driver_id: Optional[int] = Field(None, example=2)
    vehicle_id: Optional[int] = Field(None, example=3)
    status: Optional[MissionStatus] = Field(None, example="IN_PROGRESS")
    route_map_url: Optional[str] = Field(None, example="https://maps.google.com/route/456")
    notes: Optional[str] = Field(None, example="Updated priority for items")

# Schema for returning mission details
class MissionResponse(BaseModel):
    id: int
    driver_id: int
    vehicle_id: int
    status: MissionStatus
    distance: float
    total_load: float
    route_map_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    notes: Optional[str]
    orders: List[int]

    class Config:
        from_attributes = True

# Schema for mission assignment (used when assigning a driver or vehicle)
class MissionAssignment(BaseModel):
    mission_id: int
    driver_id: int
    vehicle_id: int
    message: str = Field(default="Mission assignment successful.")

# Schema for deleting a mission
class MissionDelete(BaseModel):
    id: int
    message: str = Field(default="Mission deleted successfully.")
