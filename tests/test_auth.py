"""
Integration tests for authentication endpoints.

Tests the complete authentication flow including registration,
login, token refresh, and logout.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthEndpoints:
    """Test suite for authentication endpoints."""
    
    async def test_register_user(self, client: AsyncClient, test_user_data: dict):
        """
        Test user registration.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        response = await client.post(
            "/api/v1/register",
            json=test_user_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == test_user_data["email"]
        assert data["data"]["first_name"] == test_user_data["first_name"]
        assert "hashed_password" not in data["data"]
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user_data: dict):
        """
        Test registration with duplicate email.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        # Register first time
        await client.post("/api/v1/register", json=test_user_data)
        
        # Try to register again with same email
        response = await client.post(
            "/api/v1/register",
            json=test_user_data
        )
        
        assert response.status_code == 409
    
    async def test_login_success(self, client: AsyncClient, test_user_data: dict):
        """
        Test successful login.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        # Register user first
        await client.post("/api/v1/register", json=test_user_data)
        
        # Login
        response = await client.post(
            "/api/v1/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
    
    async def test_login_invalid_credentials(self, client: AsyncClient, test_user_data: dict):
        """
        Test login with invalid credentials.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        response = await client.post(
            "/api/v1/login",
            data={
                "username": test_user_data["email"],
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
    
    async def test_get_current_user(self, client: AsyncClient, test_user_data: dict):
        """
        Test getting current user info.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        # Register and login
        await client.post("/api/v1/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        token = login_response.json()["data"]["access_token"]
        
        # Get current user
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == test_user_data["email"]
    
    async def test_refresh_token(self, client: AsyncClient, test_user_data: dict):
        """
        Test token refresh.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        # Register and login
        await client.post("/api/v1/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Refresh token
        response = await client.post(
            "/api/v1/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
    
    async def test_logout(self, client: AsyncClient, test_user_data: dict):
        """
        Test logout.
        
        Args:
            client: Test client
            test_user_data: Test user data
        """
        # Register and login
        await client.post("/api/v1/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )
        token = login_response.json()["data"]["access_token"]
        
        # Logout
        response = await client.post(
            "/api/v1/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # Try to use the token after logout
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
