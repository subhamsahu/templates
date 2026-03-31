from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # SQLite for development, switch to PostgreSQL URL in production
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
