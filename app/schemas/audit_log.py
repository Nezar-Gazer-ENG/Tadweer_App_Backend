from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating an audit log entry
class AuditLogCreate(BaseModel):
    user_id: int = Field(..., example=1)
    action: str = Field(..., example="Order Created")
    description: Optional[str] = Field(None, example="Created a new order with ID 101")
    ip_address: Optional[str] = Field(None, example="192.168.1.1")

# Schema for returning audit log details
class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    description: Optional[str]
    timestamp: datetime
    ip_address: Optional[str]

    class Config:
        from_attributes = True

# Schema for filtering audit logs
class AuditLogFilter(BaseModel):
    user_id: Optional[int] = Field(None, example=1)
    action: Optional[str] = Field(None, example="Order Created")
    start_date: Optional[datetime] = Field(None, example="2025-05-01T00:00:00")
    end_date: Optional[datetime] = Field(None, example="2025-05-15T23:59:59")

# Schema for deleting an audit log entry
class AuditLogDelete(BaseModel):
    id: int
    message: str = Field(default="Audit log entry deleted successfully.")
