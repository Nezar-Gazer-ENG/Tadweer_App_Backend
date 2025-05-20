from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    license_plate = Column(String(50), unique=True, nullable=False)
    capacity = Column(Float, nullable=False)  # Maximum load capacity (in kg or tons)
    current_load = Column(Float, default=0.0)  # Current load of the vehicle
    assigned_driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_available = Column(Boolean, default=True)

    # Relationships
    driver = relationship("User", back_populates="vehicles")  # Driver assigned to the vehicle
    missions = relationship("Mission", back_populates="vehicle", cascade="all, delete-orphan")  # Missions using this vehicle

    def __repr__(self):
        return (f"<Vehicle(id={self.id}, name='{self.name}', license_plate='{self.license_plate}', "
                f"capacity={self.capacity}, available={self.is_available})>")
