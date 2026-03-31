import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine  # noqa: F401 – kept for Alembic metadata access
from app import models  # noqa: F401 – registers all ORM models with Base.metadata
from app.routers import auth, users, permissions

# Auto-create tables for SQLite (local dev) only.
# On PostgreSQL (production/Render), Alembic migrations manage the schema.
from app.config import get_settings as _get_settings
if _get_settings().database_url.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Application Base Template",
    description="Production-ready API template with authentication, user management, and role-based permissions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers - Core authentication and user management only
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(permissions.router)
# Add your custom business logic routers here


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Application Base Template API"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
