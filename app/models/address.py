from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String(50), nullable=True)  # e.g., Home, Work
    address_line = Column(String(255), nullable=False)  # Full address as a single string
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    latitude = Column(Float, nullable=False)  # Latitude from Google Maps
    longitude = Column(Float, nullable=False)  # Longitude from Google Maps
    place_id = Column(String(100), nullable=True)  # Unique identifier from Google Maps
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="addresses")  # Link to the user who owns the address
    orders = relationship("Order", back_populates="address", cascade="all, delete-orphan")  # Orders associated with this address

    def __repr__(self):
        return (f"<Address(id={self.id}, label='{self.label}', address_line='{self.address_line}', "
                f"latitude={self.latitude}, longitude={self.longitude})>")
