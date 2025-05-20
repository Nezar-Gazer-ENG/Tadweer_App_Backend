from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models import Base

# Enum for order status
class OrderStatus(PyEnum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=True)  
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text, nullable=True)

    # Relationships
    customer = relationship("User", back_populates="orders")  # Customer placing the order
    address = relationship("Address", back_populates="orders")  # Address related to the order
    mission = relationship("Mission", back_populates="orders")  # Mission associated with the order
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # Items within the order

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, status='{self.status.name}')>"
