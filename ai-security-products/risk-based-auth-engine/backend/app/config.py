"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Production-grade application settings."""
    
    # App
    app_name: str = "Risk-Based Authentication Engine"
    debug: bool = False
    environment: str = "production"
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/riskauth"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl_seconds: int = 86400  # 24 hours
    
    # JWT
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    # Risk Engine
    max_login_velocity_minutes: int = 60
    geo_anomaly_km_threshold: int = 500
    baseline_learning_days: int = 14
    
    # GeoIP
    geoip_db_path: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
