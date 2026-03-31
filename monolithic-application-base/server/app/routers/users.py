from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app import models, schemas
from app.auth import hash_password, require_admin

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    role: Optional[models.UserRole] = None
    password: Optional[str] = None


# ── List all users ────────────────────────────────────────────────────────────

@router.get("", response_model=List[schemas.UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    return db.query(models.User).order_by(models.User.created_at).all()


# ── Create user ───────────────────────────────────────────────────────────────

@router.post("", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = models.User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── Update user (role / password) ─────────────────────────────────────────────

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updates.role is not None:
        user.role = updates.role
    if updates.password:
        if len(updates.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        user.hashed_password = hash_password(updates.password)
    db.commit()
    db.refresh(user)
    return user


# ── Delete user ───────────────────────────────────────────────────────────────

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
