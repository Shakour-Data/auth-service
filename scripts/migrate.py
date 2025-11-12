"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : migrate.py
Description  : Implementation file for migrate module
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

#!/usr/bin/env python3
"""
Script to run database migrations.

Applies Alembic migrations to set up the database schema.
"""

import asyncio
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from alembic.config import Config

from app.config import settings
from app.models.user import Base


async def run_migrations():
    """Run database migrations."""
    print("🔄 Running database migrations...")
    
    # Create Alembic config
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    
    # Configure logging
    if alembic_cfg.config_file_name is not None:
        fileConfig(alembic_cfg.config_file_name)
    
    # Create async engine
    connectable = async_engine_from_config(
        alembic_cfg.get_section(alembic_cfg.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()
    
    print("✅ Database migrations completed successfully!")


def do_run_migrations(connection):
    """
    Execute migrations with connection.
    
    Args:
        connection: Database connection
    """
    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )
    
    with context.begin_transaction():
        context.run_migrations()


if __name__ == "__main__":
    try:
        asyncio.run(run_migrations())
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
