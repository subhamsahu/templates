from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import declarative_base
from app.config import get_settings

settings = get_settings()

# SQLite requires check_same_thread=False for FastAPI's threaded request handling.
# PostgreSQL (psycopg2) does not require this argument.
_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# SQLModel.create_engine wraps SQLAlchemy's create_engine, adding extra
# validation helpers while remaining fully compatible with SQLAlchemy models.
engine = create_engine(settings.database_url, connect_args=_connect_args, echo=False)

# Keep declarative_base so existing SQLAlchemy models continue to work unchanged.
Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a SQLModel/SQLAlchemy session per request."""
    with Session(engine) as session:
        yield session
