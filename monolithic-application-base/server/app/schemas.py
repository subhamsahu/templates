from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import UserRole


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.staff


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


# ── Permissions ───────────────────────────────────────────────────────────────

class RolePermissionsResponse(BaseModel):
    id: int
    role: UserRole
    permissions: dict
    updated_at: datetime

    class Config:
        from_attributes = True


class RolePermissionsUpdate(BaseModel):
    permissions: dict


# ─── Add Your Custom Schemas Below ───────────────────────────────────────────
# Add your application-specific Pydantic schemas here
# Example:
#
# class YourModelCreate(BaseModel):
#     name: str
#     description: Optional[str] = None
#
# class YourModelResponse(BaseModel):
#     id: int
#     name: str
#     description: Optional[str]
#     created_at: datetime
#
#     class Config:
#         from_attributes = True
