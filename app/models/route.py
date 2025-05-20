from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    start_location = Column(String(255), nullable=False)  # Starting address or coordinates
    end_location = Column(String(255), nullable=False)    # Ending address or coordinates
    distance = Column(Float, nullable=False)  # Distance in kilometers or miles
    optimized_route = Column(String(1000), nullable=True)  # JSON or serialized data of the route
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    mission = relationship("Mission", back_populates="routes")  # Link to the mission associated with this route

    def __repr__(self):
        return (f"<Route(id={self.id}, mission_id={self.mission_id}, start_location='{self.start_location}', "
                f"end_location='{self.end_location}', distance={self.distance})>")
