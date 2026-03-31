from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    employee = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.staff, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Role Permissions ──────────────────────────────────────────────────────────

# Default permission sets used when seeding the DB for the first time.
# Customize these based on your application's needs.
DEFAULT_ROLE_PERMISSIONS: dict = {
    "staff": {
        "canViewDashboard": True,
        "canViewUserManagement": False,
        "canManageUsers": False,
        "canViewSettings": True,
    },
    "employee": {
        "canViewDashboard": True,
        "canViewUserManagement": False,
        "canManageUsers": False,
        "canViewSettings": True,
    },
}


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SAEnum(UserRole), unique=True, nullable=False)
    permissions = Column(JSON, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    editor = relationship("User", foreign_keys=[updated_by])


# ─── Add Your Custom Models Below ────────────────────────────────────────────
# Add your application-specific models here
# Example:
#
# class YourModel(Base):
#     __tablename__ = "your_table"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(200), nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

