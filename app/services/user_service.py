"""
User service layer.

Business logic for user management operations.
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import logging

from app.models.user import User
from app.schemas.auth import UserResponse, UserUpdate
from gravity_common.models import PaginatedResponse, PaginationParams
from gravity_common.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class UserService:
    """
    User service for user management operations.
    
    Handles CRUD operations for users with pagination and filtering.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize user service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data
            
        Raises:
            NotFoundException: If user not found
        """
        logger.debug(f"Fetching user with ID: {user_id}")
        
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundException(message=f"User not found with ID: {user_id}")
        
        return UserResponse.model_validate(user)
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User data
            
        Raises:
            NotFoundException: If user not found
        """
        logger.debug(f"Fetching user with email: {email}")
        
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {email}")
            raise NotFoundException(message=f"User not found with email: {email}")
        
        return UserResponse.model_validate(user)
    
    async def list_users(self, pagination: PaginationParams) -> PaginatedResponse[UserResponse]:
        """
        List all users with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            Paginated list of users
        """
        logger.debug(f"Listing users - page: {pagination.page}, size: {pagination.page_size}")
        
        # Count total users
        count_result = await self.db.execute(select(func.count(User.id)))
        total = count_result.scalar() or 0
        
        # Get users for current page
        result = await self.db.execute(
            select(User)
            .offset(pagination.offset)
            .limit(pagination.page_size)
            .order_by(User.created_at.desc())
        )
        users = result.scalars().all()
        
        # Convert to response models
        user_responses = [UserResponse.model_validate(user) for user in users]
        
        # Calculate pagination metadata
        total_pages = (total + pagination.page_size - 1) // pagination.page_size if total > 0 else 0
        has_next = pagination.page < total_pages
        has_previous = pagination.page > 1
        
        return PaginatedResponse(
            items=user_responses,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """
        Update user information.
        
        Args:
            user_id: User ID
            user_data: Updated user data
            
        Returns:
            Updated user data
            
        Raises:
            NotFoundException: If user not found
        """
        logger.info(f"Updating user: {user_id}")
        
        # Get user
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundException(message=f"User not found with ID: {user_id}")
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info(f"User updated successfully: {user.email}")
        
        return UserResponse.model_validate(user)
    
    async def delete_user(self, user_id: int) -> None:
        """
        Delete user.
        
        Args:
            user_id: User ID
            
        Raises:
            NotFoundException: If user not found
        """
        logger.info(f"Deleting user: {user_id}")
        
        # Get user
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundException(message=f"User not found with ID: {user_id}")
        
        # Delete user
        await self.db.delete(user)
        await self.db.commit()
        
        logger.info(f"User deleted successfully: {user.email}")
