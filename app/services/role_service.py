"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : role_service.py
Description  : Role service layer.
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Michael Rodriguez (Security & Authentication Specialist)
Contributors      : Dr. Aisha Patel, Elena Volkov
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-05 14:00 UTC
Last Modified     : 2025-11-06 16:45 UTC
Development Time  : 4 hours 30 minutes
Review Time       : 1 hour 15 minutes
Testing Time      : 2 hours 0 minutes
Total Time        : 7 hours 45 minutes

================================================================================
COST CALCULATION (محاسبه هزینه)
================================================================================
Hourly Rate       : $150/hour (Elite Engineer Standard)
Development Cost  : 4.5 × $150 = $675.00 USD
Review Cost       : 1.25 × $150 = $187.50 USD
Testing Cost      : 2.0 × $150 = $300.00 USD
Total Cost        : $1162.50 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-05 - Michael Rodriguez - Initial implementation
v1.0.1 - 2025-11-06 - Michael Rodriguez - Added file header standard

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

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.models.user import Role, User
from app.schemas.auth import RoleCreate, RoleUpdate, RoleResponse
from gravity_common.exceptions import NotFoundException, ConflictException

logger = logging.getLogger(__name__)


class RoleService:
    """
    Role service for role and permission management.
    
    Handles CRUD operations for roles and role assignments.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize role service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def create_role(self, role_data: RoleCreate) -> RoleResponse:
        """
        Create a new role.
        
        Args:
            role_data: Role creation data
            
        Returns:
            Created role data
            
        Raises:
            ConflictException: If role already exists
        """
        logger.info(f"Creating role: {role_data.name}")
        
        # Check if role already exists
        result = await self.db.execute(
            select(Role).where(Role.name == role_data.name)
        )
        existing_role = result.scalar_one_or_none()
        
        if existing_role:
            logger.warning(f"Role already exists: {role_data.name}")
            raise ConflictException(
                message="Role already exists",
                details={"name": role_data.name}
            )
        
        # Create new role
        new_role = Role(
            name=role_data.name,
            description=role_data.description,
            permissions=role_data.permissions
        )
        
        self.db.add(new_role)
        await self.db.commit()
        await self.db.refresh(new_role)
        
        logger.info(f"Role created successfully: {new_role.name} (ID: {new_role.id})")
        
        return RoleResponse.model_validate(new_role)
    
    async def list_roles(self) -> List[RoleResponse]:
        """
        List all roles.
        
        Returns:
            List of all roles
        """
        logger.debug("Listing all roles")
        
        result = await self.db.execute(
            select(Role).order_by(Role.name)
        )
        roles = result.scalars().all()
        
        return [RoleResponse.model_validate(role) for role in roles]
    
    async def get_role_by_id(self, role_id: int) -> RoleResponse:
        """
        Get role by ID.
        
        Args:
            role_id: Role ID
            
        Returns:
            Role data
            
        Raises:
            NotFoundException: If role not found
        """
        logger.debug(f"Fetching role with ID: {role_id}")
        
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            logger.warning(f"Role not found: {role_id}")
            raise NotFoundException(message=f"Role not found with ID: {role_id}")
        
        return RoleResponse.model_validate(role)
    
    async def update_role(self, role_id: int, role_data: RoleUpdate) -> RoleResponse:
        """
        Update role.
        
        Args:
            role_id: Role ID
            role_data: Updated role data
            
        Returns:
            Updated role data
            
        Raises:
            NotFoundException: If role not found
        """
        logger.info(f"Updating role: {role_id}")
        
        # Get role
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            logger.warning(f"Role not found: {role_id}")
            raise NotFoundException(message=f"Role not found with ID: {role_id}")
        
        # Update fields
        update_data = role_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)
        
        await self.db.commit()
        await self.db.refresh(role)
        
        logger.info(f"Role updated successfully: {role.name}")
        
        return RoleResponse.model_validate(role)
    
    async def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        """
        Assign role to user.
        
        Args:
            user_id: User ID
            role_id: Role ID
            
        Raises:
            NotFoundException: If user or role not found
        """
        logger.info(f"Assigning role {role_id} to user {user_id}")
        
        # Check if user exists
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundException(message=f"User not found with ID: {user_id}")
        
        # Check if role exists
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            logger.warning(f"Role not found: {role_id}")
            raise NotFoundException(message=f"Role not found with ID: {role_id}")
        
        # Assign role
        user.role_id = role_id
        await self.db.commit()
        
        logger.info(f"Role {role.name} assigned to user {user.email}")
