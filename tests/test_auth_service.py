"""
Unit tests for AuthService.

Tests authentication business logic in isolation.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate
from gravity_common.exceptions import UnauthorizedException, ConflictException


@pytest.mark.asyncio
class TestAuthService:
    """Test suite for AuthService."""
    
    async def test_register_user(self, db_session: AsyncSession):
        """
        Test user registration.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        user_data = UserCreate(
            email="newuser@example.com",
            password="Test123!@#",
            first_name="New",
            last_name="User"
        )
        
        user = await auth_service.register_user(user_data)
        
        assert user.email == user_data.email
        assert user.first_name == user_data.first_name
        assert user.is_active is True
        assert user.is_superuser is False
    
    async def test_register_duplicate_email(self, db_session: AsyncSession):
        """
        Test registration with duplicate email.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        user_data = UserCreate(
            email="duplicate@example.com",
            password="Test123!@#",
            first_name="Test",
            last_name="User"
        )
        
        # Register first user
        await auth_service.register_user(user_data)
        
        # Try to register again with same email
        with pytest.raises(ConflictException):
            await auth_service.register_user(user_data)
    
    async def test_authenticate_user_success(self, db_session: AsyncSession):
        """
        Test successful user authentication.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        # Register user
        user_data = UserCreate(
            email="auth@example.com",
            password="Test123!@#",
            first_name="Auth",
            last_name="User"
        )
        await auth_service.register_user(user_data)
        
        # Authenticate
        user = await auth_service.authenticate_user(
            user_data.email,
            user_data.password
        )
        
        assert user is not None
        assert user.email == user_data.email
    
    async def test_authenticate_user_invalid_password(self, db_session: AsyncSession):
        """
        Test authentication with invalid password.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        # Register user
        user_data = UserCreate(
            email="wrongpwd@example.com",
            password="Test123!@#",
            first_name="Test",
            last_name="User"
        )
        await auth_service.register_user(user_data)
        
        # Try to authenticate with wrong password
        with pytest.raises(UnauthorizedException):
            await auth_service.authenticate_user(
                user_data.email,
                "WrongPassword123"
            )
    
    async def test_create_tokens(self, db_session: AsyncSession):
        """
        Test token creation.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        # Register user
        user_data = UserCreate(
            email="token@example.com",
            password="Test123!@#",
            first_name="Token",
            last_name="User"
        )
        user = await auth_service.register_user(user_data)
        
        # Create tokens
        tokens = await auth_service.create_tokens(user.id, user.email)
        
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        assert tokens["expires_in"] == 3600  # 1 hour default
    
    async def test_change_password(self, db_session: AsyncSession):
        """
        Test password change.
        
        Args:
            db_session: Test database session
        """
        auth_service = AuthService(db_session)
        
        # Register user
        user_data = UserCreate(
            email="changepwd@example.com",
            password="OldPassword123!@#",
            first_name="Change",
            last_name="Password"
        )
        user = await auth_service.register_user(user_data)
        
        # Change password
        await auth_service.change_password(
            user.id,
            "OldPassword123!@#",
            "NewPassword123!@#"
        )
        
        # Try to authenticate with old password (should fail)
        with pytest.raises(UnauthorizedException):
            await auth_service.authenticate_user(
                user_data.email,
                "OldPassword123!@#"
            )
        
        # Authenticate with new password (should succeed)
        authenticated_user = await auth_service.authenticate_user(
            user_data.email,
            "NewPassword123!@#"
        )
        
        assert authenticated_user.email == user_data.email
