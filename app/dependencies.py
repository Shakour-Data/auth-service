"""
Dependency functions for FastAPI.

Provides dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import logging

from app.models.user import User
from app.schemas.auth import UserResponse
from app.core.database import get_db
from app.core.redis_client import redis_client
from app.config import settings
from gravity_common.security import decode_access_token
from gravity_common.exceptions import UnauthorizedException

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT access token
        db: Database session
        
    Returns:
        Current user data
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Check if token is blacklisted
        is_blacklisted = await redis_client.exists(f"blacklist:{token}")
        if is_blacklisted:
            logger.warning("Attempted use of blacklisted token")
            raise credentials_exception
        
        # Decode token
        payload = decode_access_token(
            token,
            settings.JWT_SECRET_KEY,
            settings.JWT_ALGORITHM
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token missing 'sub' claim")
            raise credentials_exception
        
        # Get user from database
        result = await db.execute(
            select(User).where(User.id == int(user_id))
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            logger.warning(f"User not found for token: {user_id}")
            raise credentials_exception
        
        return UserResponse.model_validate(user)
        
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> UserResponse:
    """
    Get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        Active user data
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        logger.warning(f"Inactive user attempted access: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return current_user


async def get_current_superuser(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
) -> UserResponse:
    """
    Get current superuser.
    
    Args:
        current_user: Current active user
        
    Returns:
        Superuser data
        
    Raises:
        HTTPException: If user is not superuser
    """
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted admin access: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return current_user
