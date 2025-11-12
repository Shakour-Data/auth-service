# 🔐 Auth Service - Independent Authentication & Authorization Microservice

## Overview

**Completely independent** authentication and authorization microservice that can be used in **unlimited projects** without modification. This service handles user authentication, token management, and role-based access control using industry best practices.

## Features

✅ **JWT-based Authentication** - Secure token-based auth  
✅ **OAuth2 Password Flow** - Standard OAuth2 implementation  
✅ **Refresh Tokens** - Long-lived refresh tokens with rotation  
✅ **Token Blacklist** - Redis-based token revocation  
✅ **Role-Based Access Control (RBAC)** - Flexible role management  
✅ **Password Security** - bcrypt hashing with salt  
✅ **Rate Limiting** - Prevent brute force attacks  
✅ **PostgreSQL Database** - Reliable user storage  
✅ **Health Checks** - Monitor service health  
✅ **API Documentation** - Auto-generated Swagger UI  
✅ **Docker Ready** - Containerized deployment  
✅ **100% Independent** - No dependencies on other services  

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout (blacklist token)
- `POST /api/v1/auth/change-password` - Change user password
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password with token

### User Management
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/me` - Update current user
- `GET /api/v1/auth/users` - List all users (admin only)
- `GET /api/v1/auth/users/{user_id}` - Get user by ID (admin only)
- `DELETE /api/v1/auth/users/{user_id}` - Delete user (admin only)

### Roles & Permissions
- `GET /api/v1/auth/roles` - List all roles
- `POST /api/v1/auth/roles` - Create new role (admin only)
- `PUT /api/v1/auth/users/{user_id}/role` - Assign role to user (admin only)

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics

## Quick Start

### 1. Environment Setup

Create `.env` file:

```env
# Application
APP_NAME=auth-service
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://gravity:gravity_secret_2025@localhost:5432/auth_service

# Redis (for token blacklist)
REDIS_URL=redis://:redis_secret_2025@localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

### 2. Install Dependencies

```bash
cd auth-service
poetry install
```

### 3. Run Database Migrations

```bash
poetry run alembic upgrade head
```

### 4. Start Service

```bash
# Development
poetry run uvicorn app.main:app --reload --port 8081

# Production
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8081 --workers 4
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8081/docs
- **ReDoc**: http://localhost:8081/redoc

## Docker Deployment

```bash
# Build image
docker build -t auth-service:1.0.0 .

# Run container
docker run -d \
  --name auth-service \
  -p 8081:8081 \
  --env-file .env \
  auth-service:1.0.0
```

## Usage Examples

### Register New User

```bash
curl -X POST http://localhost:8081/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePassword123!"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Access Protected Endpoint

```bash
curl -X GET http://localhost:8081/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Integration with Other Services

This service is **completely independent** and can be integrated with any project:

### Option 1: Direct API Calls

```python
import httpx

async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://auth-service:8081/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
```

### Option 2: Token Verification Library

```python
from gravity_common.security import decode_access_token

def verify_user_token(token: str, secret_key: str):
    try:
        payload = decode_access_token(token, secret_key)
        return payload
    except Exception:
        return None
```

## Security Features

1. **Password Hashing**: bcrypt with automatic salt generation
2. **JWT Tokens**: Signed with HS256 algorithm
3. **Token Expiration**: Configurable expiration times
4. **Refresh Token Rotation**: New refresh token on each refresh
5. **Token Blacklist**: Redis-based revocation
6. **Rate Limiting**: Prevent brute force attacks
7. **CORS Protection**: Configurable allowed origins
8. **SQL Injection Prevention**: Parameterized queries
9. **Input Validation**: Pydantic models

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refresh tokens table
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

All configuration is done via environment variables (see `.env.example`).

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test
poetry run pytest tests/test_auth.py
```

## Monitoring

- **Health Check**: `GET /health`
- **Prometheus Metrics**: `GET /metrics`
- **Logs**: Structured JSON logging to stdout

## Performance

- Async/await for all I/O operations
- Connection pooling for PostgreSQL
- Redis caching for frequently accessed data
- Optimized database queries with indexes

## Scalability

- **Stateless Design**: Can run multiple instances
- **Horizontal Scaling**: Load balance across instances
- **Database**: Connection pooling supports high concurrency
- **Redis**: Shared state across instances

## License

MIT License - Use in unlimited projects without restrictions.

## Support

For issues or questions, check the main project documentation.

---

**Built with ❤️ by Gravity Elite Team**
