from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Item name, e.g., "Tire", "Battery"
    type = Column(String(50), nullable=False)  # General type, e.g., "Tire"
    subtype = Column(String(50), nullable=True)  # Specific type, e.g., "Mini", "Large"
    icon_url = Column(String(255), nullable=True)  # Optional URL for the item icon/image
    description = Column(String(255), nullable=True)  # Brief description of the item
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # ID of the user who created the item
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order_items = relationship("OrderItem", back_populates="item", cascade="all, delete-orphan")  # Associated order items
    creator = relationship("User", back_populates="items")  # Link to the user who created the item

    def __repr__(self):
        return (f"<Item(id={self.id}, name='{self.name}', type='{self.type}', "
                f"subtype='{self.subtype}', created_by={self.created_by})>")
