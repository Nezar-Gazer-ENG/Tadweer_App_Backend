from pydantic import BaseModel
from typing import Optional, List

# Pagination parameters
class Pagination(BaseModel):
    page: int = 1
    size: int = 10

# Coordinate representation for geolocation
class Coordinate(BaseModel):
    latitude: float
    longitude: float

# Status response model
class StatusResponse(BaseModel):
    status: str
    message: Optional[str] = None

# Date range filter for querying
class DateRange(BaseModel):
    start_date: str
    end_date: str

# Success message model
class SuccessMessage(BaseModel):
    message: str = "Operation completed successfully."

# Generic list response model
class ListResponse(BaseModel):
    total: int
    items: List


class MessageResponse(BaseModel):
    detail: str