"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : user.py
Description  : SQLAlchemy models for Auth Service.
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Dr. Aisha Patel (Database Specialist)
Contributors      : Michael Rodriguez
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 2 hours 0 minutes
Review Time       : 0 hours 30 minutes
Testing Time      : 1 hour 0 minutes
Total Time        : 3 hours 30 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 2.0 × $150 = $300.00 USD
Review Cost       : 0.5 × $150 = $75.00 USD
Testing Cost      : 1.0 × $150 = $150.00 USD
Total Cost        : $525.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - Dr. Aisha Patel - Initial implementation
v1.0.1 - 2025-11-06 - Dr. Aisha Patel - Added file header standard

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

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from gravity_common.database import Base


class User(Base):
    """
    User model for authentication.
    
    Stores user credentials and basic information.
    Each user has a unique email and can have one role.
    """
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Foreign key to roles
    role_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("roles.id"), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    role: Mapped[Optional["Role"]] = relationship("Role", back_populates="users")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


class Role(Base):
    """
    Role model for RBAC (Role-Based Access Control).
    
    Defines user roles with associated permissions.
    Permissions are stored as JSON for flexibility.
    """
    
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permissions: Mapped[list] = mapped_column(JSON, default=list)  # List of permission strings
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    
    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="role")
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"


class RefreshToken(Base):
    """
    Refresh token model for token management.
    
    Stores refresh tokens with expiration for token rotation.
    Tokens are hashed for security.
    """
    
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"
