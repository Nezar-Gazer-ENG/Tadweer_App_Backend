from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)  # Price per unit of the item
    total_price = Column(Float, nullable=False)  # Calculated as quantity * unit_price
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="order_items")  # Link to the order this item belongs to
    item = relationship("Item", back_populates="order_items")  # Link to the specific item

    def __repr__(self):
        return (f"<OrderItem(id={self.id}, order_id={self.order_id}, item_id={self.item_id}, "
                f"quantity={self.quantity}, total_price={self.total_price})>")
