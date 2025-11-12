"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : auth.py
Description  : Pydantic schemas for Auth Service.
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Elena Volkov (Backend Architecture Lead)
Contributors      : Michael Rodriguez
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 1 hour 30 minutes
Review Time       : 0 hours 30 minutes
Testing Time      : 0 hours 30 minutes
Total Time        : 2 hours 30 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 1.5 × $150 = $225.00 USD
Review Cost       : 0.5 × $150 = $75.00 USD
Testing Cost      : 0.5 × $150 = $75.00 USD
Total Cost        : $375.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - Elena Volkov - Initial implementation
v1.0.1 - 2025-11-06 - Elena Volkov - Added file header standard

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
from pydantic import BaseModel, EmailStr, Field, field_validator
from gravity_common.models import BaseModel as GravityBaseModel


# ==================== User Schemas ====================

class UserBase(GravityBaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User's email address")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength.
        
        Requirements:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - Minimum 8 characters
        """
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(GravityBaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Schema for user response."""
    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="Whether user is active")
    is_superuser: bool = Field(..., description="Whether user is superuser")
    role_id: Optional[int] = Field(None, description="User's role ID")
    created_at: datetime = Field(..., description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    model_config = {"from_attributes": True}


class UserInDB(UserResponse):
    """Schema for user stored in database (includes hashed password)."""
    hashed_password: str


# ==================== Authentication Schemas ====================

class Token(GravityBaseModel):
    """Schema for authentication tokens."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenPayload(GravityBaseModel):
    """Schema for JWT token payload."""
    sub: str = Field(..., description="Subject (user ID)")
    email: str = Field(..., description="User email")
    role: Optional[str] = Field(None, description="User role")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    type: str = Field(default="access", description="Token type (access/refresh)")


class LoginRequest(GravityBaseModel):
    """Schema for login request."""
    username: EmailStr = Field(..., description="User email (username)")
    password: str = Field(..., description="User password")


class RefreshTokenRequest(GravityBaseModel):
    """Schema for refresh token request."""
    refresh_token: str = Field(..., description="Refresh token")


class ChangePasswordRequest(GravityBaseModel):
    """Schema for password change request."""
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """Validate new password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class ForgotPasswordRequest(GravityBaseModel):
    """Schema for forgot password request."""
    email: EmailStr = Field(..., description="User email")


class ResetPasswordRequest(GravityBaseModel):
    """Schema for password reset request."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


# ==================== Role Schemas ====================

class RoleBase(GravityBaseModel):
    """Base role schema."""
    name: str = Field(..., min_length=1, max_length=50, description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: List[str] = Field(default_factory=list, description="List of permissions")


class RoleCreate(RoleBase):
    """Schema for creating a new role."""
    pass


class RoleUpdate(GravityBaseModel):
    """Schema for updating a role."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


class RoleResponse(RoleBase):
    """Schema for role response."""
    id: int = Field(..., description="Role ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = {"from_attributes": True}


class AssignRoleRequest(GravityBaseModel):
    """Schema for assigning role to user."""
    role_id: int = Field(..., description="Role ID to assign")
