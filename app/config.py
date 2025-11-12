"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : config.py
Description  : Configuration settings for Auth Service
Language     : English (UK)
Framework    : FastAPI / Python 3.12+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : Elite Engineering Team
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-12 00:00 UTC
Last Modified     : 2025-11-12 00:00 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-12 - Dr. Sarah Chen - Standardized configuration
v1.0.1 - 2025-11-12 - Auto-generated with proper type hints and validation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : None
External  : pydantic-settings>=2.0.0, pydantic>=2.0.0
Database  : PostgreSQL 16+, Redis 7

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/05-auth-service

================================================================================
"""

from typing import Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables or .env file.
    Follows 12-factor app configuration principles.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # ==============================================================================
    # Application Configuration
    # ==============================================================================
    APP_NAME: str = Field(default="05-auth-service", description="Service name")
    APP_VERSION: str = Field(default="1.0.0", description="Service version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    PORT: int = Field(default=8005, description="Application port")
    
    # ==============================================================================
    # Database Configuration (PostgreSQL)
    # ==============================================================================
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5405/auth_service",
        description="PostgreSQL connection URL"
    )
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5405, description="Database port")
    DB_NAME: str = Field(default="auth_service", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="postgres", description="Database password")
    DB_POOL_SIZE: int = Field(default=10, description="Connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, description="Max pool overflow")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Pool timeout in seconds")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # ==============================================================================
    # Redis Configuration
    # ==============================================================================
    REDIS_URL: str = Field(
        default="redis://localhost:6305/0",
        description="Redis connection URL"
    )
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6305, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Max Redis connections")
    
    # ==============================================================================
    # Security Configuration
    # ==============================================================================
    SECRET_KEY: str = Field(
        default="change-in-production-min-32-chars-12345",
        min_length=32,
        description="Application secret key"
    )
    JWT_SECRET_KEY: str = Field(
        default="change-jwt-secret-in-production-12345",
        min_length=32,
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration in days"
    )
    
    # ==============================================================================
    # CORS Configuration
    # ==============================================================================
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Comma-separated list of allowed origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Allow credentials in CORS"
    )
    CORS_ALLOW_METHODS: str = Field(
        default="GET,POST,PUT,DELETE,PATCH,OPTIONS",
        description="Allowed HTTP methods"
    )
    CORS_ALLOW_HEADERS: str = Field(default="*", description="Allowed headers")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # ==============================================================================
    # Rate Limiting
    # ==============================================================================
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Requests per minute")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, description="Requests per hour")
    
    # ==============================================================================
    # Service Discovery (Consul)
    # ==============================================================================
    CONSUL_HOST: str = Field(default="localhost", description="Consul host")
    CONSUL_PORT: int = Field(default=8500, description="Consul port")
    SERVICE_DISCOVERY_ENABLED: bool = Field(
        default=False,
        description="Enable service discovery"
    )
    
    # ==============================================================================
    # External Services URLs
    # ==============================================================================
    API_GATEWAY_URL: str = Field(
        default="http://localhost:8003",
        description="API Gateway URL"
    )
    AUTH_SERVICE_URL: str = Field(
        default="http://localhost:8005",
        description="Auth Service URL"
    )
    USER_SERVICE_URL: str = Field(
        default="http://localhost:8006",
        description="User Service URL"
    )
    NOTIFICATION_SERVICE_URL: str = Field(
        default="http://localhost:8007",
        description="Notification Service URL"
    )
    
    # ==============================================================================
    # Monitoring & Observability
    # ==============================================================================
    METRICS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: int = Field(default=9090, description="Metrics port")
    TRACING_ENABLED: bool = Field(default=False, description="Enable Jaeger tracing")
    JAEGER_HOST: str = Field(default="localhost", description="Jaeger host")
    JAEGER_PORT: int = Field(default=6831, description="Jaeger port")
    
    # ==============================================================================
    # Testing Configuration
    # ==============================================================================
    TEST_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/test_auth_service",
        description="Test database URL"
    )
    TEST_REDIS_URL: str = Field(
        default="redis://localhost:6379/15",
        description="Test Redis URL"
    )
    
    # ==============================================================================
    # API Documentation
    # ==============================================================================
    API_TITLE: str = Field(
        default="Auth Service API",
        description="API title"
    )
    API_DESCRIPTION: str = Field(
        default="Independent Auth Service Microservice",
        description="API description"
    )
    API_VERSION: str = Field(default="1.0.0", description="API version")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the accepted values."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()
    
    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_keys(cls, v: str) -> str:
        """Ensure secret keys are not default values in production."""
        if "change" in v.lower() or "secret" in v.lower():
            import os
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError("Must set secure SECRET_KEY in production")
        return v


# ==============================================================================
# Service-Specific Configuration
# ==============================================================================
class AuthServiceSettings(Settings):
    """Extended settings for Auth Service."""
    
    # OAuth2 providers
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth secret")
    GITHUB_CLIENT_ID: Optional[str] = Field(default=None, description="GitHub OAuth client ID")
    GITHUB_CLIENT_SECRET: Optional[str] = Field(default=None, description="GitHub OAuth secret")
    
    # Password policy
    PASSWORD_MIN_LENGTH: int = Field(default=8, description="Minimum password length")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(default=True, description="Require uppercase")
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(default=True, description="Require lowercase")
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True, description="Require digit")
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True, description="Require special character")
    
    # Session
    SESSION_COOKIE_NAME: str = Field(default="session_id", description="Session cookie name")
    SESSION_EXPIRE_SECONDS: int = Field(default=3600, description="Session expiration")


settings = AuthServiceSettings()


# ==============================================================================
# Global Settings Instance
# ==============================================================================
settings = Settings()


# ==============================================================================
# Configuration Validation on Import
# ==============================================================================
if __name__ == "__main__":
    # Print configuration (excluding sensitive data)
    print(f"✅ Configuration loaded for: {settings.APP_NAME}")
    print(f"   Version: {settings.APP_VERSION}")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Port: {settings.PORT}")
    print(f"   Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"   Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    print(f"   Debug Mode: {settings.DEBUG}")
    print(f"   Log Level: {settings.LOG_LEVEL}")