from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
from app.database import get_db
from app import models
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/permissions", tags=["Permissions"])

# ── Schemas ────────────────────────────────────────────────────────────────────

class RolePermissionsResponse(BaseModel):
    role: str
    permissions: Dict[str, bool]
    updated_at: str | None = None

    class Config:
        from_attributes = True


class PermissionsUpdateRequest(BaseModel):
    permissions: Dict[str, bool]


# ── Helpers ────────────────────────────────────────────────────────────────────

def _ensure_seeded(db: Session) -> None:
    """Insert default permissions rows if they don't exist yet."""
    for role_name, perm_dict in models.DEFAULT_ROLE_PERMISSIONS.items():
        role = models.UserRole(role_name)
        exists = db.query(models.RolePermissions).filter(
            models.RolePermissions.role == role
        ).first()
        if not exists:
            db.add(models.RolePermissions(role=role, permissions=perm_dict))
    db.commit()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("", response_model=Dict[str, Dict[str, bool]])
def get_all_permissions(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),  # any authenticated user
):
    """Return permissions map for every configurable role (staff, employee)."""
    _ensure_seeded(db)
    rows = db.query(models.RolePermissions).all()
    return {row.role.value: row.permissions for row in rows}


@router.put("/{role}", response_model=Dict[str, bool])
def update_role_permissions(
    role: str,
    body: PermissionsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    """Update permissions for a configurable role (admin only)."""
    if role == "admin":
        raise HTTPException(status_code=400, detail="Admin permissions cannot be changed")

    try:
        role_enum = models.UserRole(role)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Role '{role}' not found")

    _ensure_seeded(db)
    row = db.query(models.RolePermissions).filter(
        models.RolePermissions.role == role_enum
    ).first()

    if not row:
        raise HTTPException(status_code=404, detail="Permissions record not found")

    row.permissions = body.permissions
    row.updated_by = current_user.id
    db.commit()
    db.refresh(row)
    return row.permissions
