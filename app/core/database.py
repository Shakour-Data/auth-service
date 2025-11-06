"""
Database configuration and session management.

Provides async database connection and session management for Auth Service.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from gravity_common.database import DatabaseConfig
from app.config import settings


# Initialize database configuration
db_manager = DatabaseConfig(
    database_url=settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.
    
    Yields:
        AsyncSession: Database session
    """
    async for session in db_manager.get_session():
        yield session
