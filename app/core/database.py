"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : database.py
Description  : Database configuration and session management.
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : None
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 0 hours 30 minutes
Review Time       : 0 hours 15 minutes
Testing Time      : 0 hours 15 minutes
Total Time        : 1 hour 0 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 0.5 × $150 = $75.00 USD
Review Cost       : 0.25 × $150 = $37.50 USD
Testing Cost      : 0.25 × $150 = $37.50 USD
Total Cost        : $150.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - Dr. Sarah Chen - Initial implementation
v1.0.1 - 2025-11-06 - Dr. Sarah Chen - Added file header standard

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : gravity_common (where applicable)
External  : FastAPI, SQLAlchemy, Pydantic (as needed)
Database  : PostgreSQL 16+, Redis 7 (as needed)

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/GravityMicroServices

================================================================================
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
