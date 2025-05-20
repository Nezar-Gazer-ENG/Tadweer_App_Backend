from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models import Base

# Enum for notification type
class NotificationType(PyEnum):
    ORDER_UPDATE = "ORDER_UPDATE"
    MISSION_UPDATE = "MISSION_UPDATE"
    GENERAL = "GENERAL"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)  # Notification message content
    type = Column(Enum(NotificationType), default=NotificationType.GENERAL, nullable=False)
    is_read = Column(Boolean, default=False)  # Mark notification as read or unread
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    recipient = relationship("User", back_populates="notifications")  # User receiving the notification

    def __repr__(self):
        return (f"<Notification(id={self.id}, recipient_id={self.recipient_id}, "
                f"type='{self.type.name}', is_read={self.is_read})>")
