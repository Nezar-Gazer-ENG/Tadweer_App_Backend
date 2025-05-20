from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new vehicle
class VehicleCreate(BaseModel):
    name: str = Field(..., example="Truck A")
    license_plate: str = Field(..., example="XYZ-1234")
    capacity: float = Field(..., example=1000.0)  # in kg
    assigned_driver_id: Optional[int] = Field(None, example=1)
    is_available: bool = Field(default=True)

# Schema for updating an existing vehicle
class VehicleUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Truck B")
    license_plate: Optional[str] = Field(None, example="ABC-5678")
    capacity: Optional[float] = Field(None, example=1200.0)
    assigned_driver_id: Optional[int] = Field(None, example=2)
    is_available: Optional[bool] = Field(None, example=False)

# Schema for returning vehicle details
class VehicleResponse(BaseModel):
    id: int
    name: str
    license_plate: str
    capacity: float
    current_load: float
    assigned_driver_id: Optional[int]
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schema for deleting a vehicle
class VehicleDelete(BaseModel):
    id: int
    message: str = Field(default="Vehicle deleted successfully.")
