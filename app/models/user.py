from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.models import Base

# Enum for user roles
class UserRole(PyEnum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    DRIVER = "DRIVER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships: Customer Role
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    # Relationships: Driver Role
    missions = relationship("Mission", back_populates="driver", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="driver", cascade="all, delete-orphan")
    assignment_logs = relationship("MissionAssignmentLog", back_populates="driver", cascade="all, delete-orphan")

    # Relationships: Admin/Moderator Role
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

    # Relationships: Notifications (all roles)
    notifications = relationship("Notification", back_populates="recipient", cascade="all, delete-orphan")

    # Relationships: Items created by user (usually admins or authorized users)
    items = relationship("Item", back_populates="creator", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.name}')>"
