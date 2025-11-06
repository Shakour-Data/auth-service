# Auth Service - Development & Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- PostgreSQL 16+
- Redis 7+

### Installation

1. **Install dependencies:**
```bash
cd auth-service
poetry install
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run database migrations:**
```bash
poetry run alembic upgrade head
```

4. **Create a superuser:**
```bash
poetry run python scripts/create_superuser.py
```

5. **Start the service:**
```bash
poetry run uvicorn app.main:create_app --factory --reload --host 0.0.0.0 --port 8000
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t gravity-auth-service:latest .
```

### Run Container
```bash
docker run -d \
  --name auth-service \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/auth_db \
  -e REDIS_URL=redis://redis:6379/0 \
  -e JWT_SECRET_KEY=your-secret-key \
  gravity-auth-service:latest
```

### Using Docker Compose
```bash
# From root directory
docker-compose up -d postgres redis
docker-compose up -d auth-service
```

## 🧪 Testing

### Run All Tests
```bash
poetry run pytest
```

### Run with Coverage
```bash
poetry run pytest --cov=app --cov-report=html --cov-report=term
```

### Run Specific Test File
```bash
poetry run pytest tests/test_auth.py -v
```

## 📚 API Documentation

Once running, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## 🔧 Development

### Database Migrations

Create a new migration:
```bash
poetry run alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
poetry run alembic upgrade head
```

Rollback migration:
```bash
poetry run alembic downgrade -1
```

### Code Quality

Format code:
```bash
poetry run black app/ tests/
```

Type checking:
```bash
poetry run mypy app/
```

Linting:
```bash
poetry run ruff check app/
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Metrics (Prometheus)
```
http://localhost:8000/metrics
```

## 🔐 Security

### JWT Configuration
- Access tokens expire in 1 hour (configurable via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`)
- Refresh tokens expire in 7 days (configurable via `JWT_REFRESH_TOKEN_EXPIRE_DAYS`)
- Tokens are blacklisted on logout using Redis

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## 🌐 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | ✅ |
| `REDIS_URL` | Redis connection string | - | ✅ |
| `JWT_SECRET_KEY` | Secret key for JWT signing | - | ✅ |
| `JWT_ALGORITHM` | JWT algorithm | HS256 | ❌ |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry | 60 | ❌ |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | 7 | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins | * | ❌ |
| `LOG_LEVEL` | Logging level | INFO | ❌ |
| `ENVIRONMENT` | Environment (dev/prod) | development | ❌ |

## 📝 API Endpoints

### Authentication
- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - Login with credentials
- `POST /api/v1/refresh` - Refresh access token
- `POST /api/v1/logout` - Logout (blacklist token)
- `GET /api/v1/me` - Get current user info
- `POST /api/v1/change-password` - Change password
- `POST /api/v1/forgot-password` - Request password reset
- `POST /api/v1/reset-password` - Reset password

### User Management (Admin)
- `GET /api/v1/users` - List users (paginated)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Role Management (Admin)
- `GET /api/v1/roles` - List all roles
- `POST /api/v1/roles` - Create new role
- `PUT /api/v1/users/{user_id}/role` - Assign role to user

## 🐛 Troubleshooting

### Database Connection Issues
1. Verify PostgreSQL is running: `docker-compose ps postgres`
2. Check DATABASE_URL in `.env`
3. Test connection: `psql $DATABASE_URL`

### Redis Connection Issues
1. Verify Redis is running: `docker-compose ps redis`
2. Check REDIS_URL in `.env`
3. Test connection: `redis-cli -u $REDIS_URL ping`

### Migration Issues
1. Check database exists: `psql -l | grep auth_db`
2. Reset migrations: `poetry run alembic downgrade base && poetry run alembic upgrade head`

## 📦 Production Deployment

### Kubernetes
See `kubernetes/` directory for deployment manifests.

### Performance Tuning
- Use `--workers 4` for uvicorn (adjust based on CPU cores)
- Configure connection pooling in database settings
- Enable Redis connection pooling
- Use CDN for static assets

### Security Checklist
- [ ] Change default JWT_SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable SSL/TLS for database connections
- [ ] Configure CORS_ORIGINS properly
- [ ] Set up rate limiting
- [ ] Enable request logging
- [ ] Configure firewall rules
- [ ] Use secrets management (e.g., Vault)

## 📄 License

Copyright © 2024 Gravity MicroServices Team
