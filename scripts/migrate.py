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
        alembic_cfg.get_section(alembic_cfg.config_ini_section),
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
