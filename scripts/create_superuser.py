#!/usr/bin/env python3
"""
Script to create a superuser account.

Creates an admin account for initial system access.
"""

import asyncio
import sys
from getpass import getpass

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate
from gravity_common.exceptions import ConflictException


async def create_superuser():
    """Create a superuser account interactively."""
    print("🔐 Creating superuser account...\n")
    
    # Get user input
    email = input("Enter email: ").strip()
    if not email:
        print("❌ Email is required!")
        sys.exit(1)
    
    password = getpass("Enter password: ").strip()
    if not password:
        print("❌ Password is required!")
        sys.exit(1)
    
    password_confirm = getpass("Confirm password: ").strip()
    if password != password_confirm:
        print("❌ Passwords do not match!")
        sys.exit(1)
    
    first_name = input("Enter first name (optional): ").strip() or None
    last_name = input("Enter last name (optional): ").strip() or None
    
    # Create user
    try:
        async for session in get_async_session():
            auth_service = AuthService(session)
            
            user_data = UserCreate(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            user = await auth_service.register_user(user_data, is_superuser=True)
            
            print(f"\n✅ Superuser created successfully!")
            print(f"   Email: {user.email}")
            print(f"   ID: {user.id}")
            print(f"   Superuser: {user.is_superuser}")
            
            break
    
    except ConflictException:
        print(f"\n❌ User with email '{email}' already exists!")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Failed to create superuser: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_superuser())
