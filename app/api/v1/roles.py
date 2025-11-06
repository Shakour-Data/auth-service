"""
Role management API endpoints.

Admin-only endpoints for managing roles and permissions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import logging

from app.schemas.auth import RoleCreate, RoleUpdate, RoleResponse, AssignRoleRequest
from app.services.role_service import RoleService
from app.core.database import get_db
from app.dependencies import get_current_superuser
from gravity_common.models import ApiResponse
from gravity_common.exceptions import NotFoundException, ConflictException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/roles",
    response_model=ApiResponse[List[RoleResponse]],
    summary="List all roles",
    description="Get list of all roles",
    responses={
        200: {"description": "Roles retrieved successfully"}
    }
)
async def list_roles(
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[List[RoleResponse]]:
    """
    List all roles.
    
    Available to all authenticated users.
    
    Args:
        db: Database session
        
    Returns:
        List of roles
    """
    logger.debug("List roles request")
    
    try:
        role_service = RoleService(db)
        roles = await role_service.list_roles()
        
        return ApiResponse(
            success=True,
            data=roles,
            message="Roles retrieved successfully"
        )
    
    except Exception as e:
        logger.exception(f"Error listing roles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/roles",
    response_model=ApiResponse[RoleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create new role",
    description="Create a new role with permissions (admin only)",
    responses={
        201: {"description": "Role created successfully"},
        409: {"description": "Role already exists"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized (admin only)"}
    }
)
async def create_role(
    role_data: RoleCreate,
    current_user: Annotated[object, Depends(get_current_superuser)],
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[RoleResponse]:
    """
    Create a new role.
    
    Requires superuser privileges.
    
    Args:
        role_data: Role creation data
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Created role data
    """
    logger.info(f"Create role request: {role_data.name}")
    
    try:
        role_service = RoleService(db)
        role = await role_service.create_role(role_data)
        
        return ApiResponse(
            success=True,
            data=role,
            message="Role created successfully"
        )
    
    except ConflictException as e:
        logger.warning(f"Role creation failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    
    except Exception as e:
        logger.exception(f"Error creating role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put(
    "/users/{user_id}/role",
    response_model=ApiResponse[object],
    summary="Assign role to user",
    description="Assign a role to a user (admin only)",
    responses={
        200: {"description": "Role assigned successfully"},
        404: {"description": "User or role not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized (admin only)"}
    }
)
async def assign_role_to_user(
    user_id: int,
    assign_data: AssignRoleRequest,
    current_user: Annotated[object, Depends(get_current_superuser)],
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[object]:
    """
    Assign role to user.
    
    Requires superuser privileges.
    
    Args:
        user_id: User ID
        assign_data: Role assignment data
        current_user: Current authenticated superuser
        db: Database session
        
    Returns:
        Success message
    """
    logger.info(f"Assign role request - user: {user_id}, role: {assign_data.role_id}")
    
    try:
        role_service = RoleService(db)
        await role_service.assign_role_to_user(user_id, assign_data.role_id)
        
        return ApiResponse(
            success=True,
            message="Role assigned successfully"
        )
    
    except NotFoundException as e:
        logger.warning(f"Role assignment failed: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    
    except Exception as e:
        logger.exception(f"Error assigning role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
