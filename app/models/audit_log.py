from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # Action performed (e.g., "Create Order", "Update Mission")
    description = Column(String(255), nullable=True)  # Detailed description of the action
    timestamp = Column(DateTime, default=datetime.utcnow)  # Time when the action was logged
    ip_address = Column(String(50), nullable=True)  # IP address from which the action was performed

    # Relationships
    user = relationship("User", back_populates="audit_logs")  # User who performed the action

    def __repr__(self):
        return (f"<AuditLog(id={self.id}, user_id={self.user_id}, action='{self.action}', "
                f"timestamp={self.timestamp}, ip_address='{self.ip_address}')>")
