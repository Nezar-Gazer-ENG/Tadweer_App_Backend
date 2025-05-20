from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum for notification type
class NotificationType(str, Enum):
    ORDER_UPDATE = "ORDER_UPDATE"
    MISSION_ASSIGNMENT = "MISSION_ASSIGNMENT"
    MISSION_COMPLETION = "MISSION_COMPLETION"
    GENERAL = "GENERAL"

# Schema for creating a new notification
class NotificationCreate(BaseModel):
    recipient_id: int = Field(..., example=1)
    message: str = Field(..., example="Your order has been assigned to a driver.")
    type: NotificationType = Field(..., example="ORDER_UPDATE")

# Schema for updating an existing notification
class NotificationUpdate(BaseModel):
    is_read: bool = Field(..., example=True)

# Schema for returning notification details
class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Schema for marking a notification as read
class NotificationMarkRead(BaseModel):
    notification_id: int
    message: str = Field(default="Notification marked as read.")

# Schema for deleting a notification
class NotificationDelete(BaseModel):
    id: int
    message: str = Field(default="Notification deleted successfully.")
