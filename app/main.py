"""
FastAPI application factory and configuration.

Creates and configures the FastAPI application instance.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.api.v1 import auth, users, roles
from app.core.database import db_manager
from app.core.redis_client import redis_client
from gravity_common.exceptions import GravityException
from gravity_common.logging_config import setup_logging


# Setup logging
logger = setup_logging(
    service_name=settings.APP_NAME,
    log_level=settings.LOG_LEVEL,
    json_logs=not settings.DEBUG,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager for startup and shutdown events.
    
    Handles initialization and cleanup of database and Redis connections.
    """
    logger.info(f"Starting {settings.APP_NAME}...")
    
    # Initialize Redis
    await redis_client.connect()
    logger.info("Redis connection established")
    
    # Database is initialized lazily on first request
    logger.info(f"{settings.APP_NAME} started successfully")
    
    yield
    
    # Cleanup
    logger.info(f"Shutting down {settings.APP_NAME}...")
    await redis_client.disconnect()
    await db_manager.close()
    logger.info(f"{settings.APP_NAME} shut down successfully")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add Prometheus instrumentation
if settings.PROMETHEUS_ENABLED:
    Instrumentator().instrument(app).expose(app)


# Exception handlers
@app.exception_handler(GravityException)
async def gravity_exception_handler(request, exc: GravityException):
    """Handle custom Gravity exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "details": exc.details,
        },
    )


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(roles.router, prefix=settings.API_V1_PREFIX, tags=["Roles"])


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the service and its dependencies.
    """
    # Check database
    db_healthy = await db_manager.health_check()
    
    # Check Redis
    redis_healthy = await redis_client.health_check()
    
    status = "healthy" if db_healthy and redis_healthy else "unhealthy"
    
    return {
        "status": status,
        "service": settings.APP_NAME,
        "version": settings.API_VERSION,
        "dependencies": {
            "database": "healthy" if db_healthy else "unhealthy",
            "redis": "healthy" if redis_healthy else "unhealthy",
        },
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": settings.APP_NAME,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "health": "/health",
    }
