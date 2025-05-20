from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Schema for creating a new route
class RouteCreate(BaseModel):
    mission_id: int = Field(..., example=1)
    start_location: str = Field(..., example="24.7136, 46.6753")
    end_location: str = Field(..., example="21.4225, 39.8262")
    distance: float = Field(..., example=350.5)  # in kilometers
    optimized_route: Optional[List[str]] = Field(None, example=["Location A", "Location B", "Location C"])

# Schema for updating an existing route
class RouteUpdate(BaseModel):
    optimized_route: Optional[List[str]] = Field(None, example=["Location A", "Location B", "Location C", "Location D"])
    distance: Optional[float] = Field(None, example=400.0)

# Schema for returning route details
class RouteResponse(BaseModel):
    id: int
    mission_id: int
    start_location: str
    end_location: str
    distance: float
    optimized_route: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True

# Schema for deleting a route
class RouteDelete(BaseModel):
    id: int
    message: str = Field(default="Route deleted successfully.")
