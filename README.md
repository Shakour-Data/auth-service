# auth-service

## 📋 Description
Authentication & Authorization service

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker & Docker Compose

### Installation

```bash
# 1. Clone repository
git clone https://github.com/gravity/auth-service.git
cd auth-service

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 3. Install dependencies
poetry install

# 4. Start infrastructure
docker-compose up -d

# 5. Run migrations (if applicable)
poetry run alembic upgrade head

# 6. Start service
poetry run uvicorn app.main:create_app --factory --reload --port 8001
```

## 📚 API Documentation
Once running, access:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html
```

## 🐳 Docker

```bash
# Build image
docker build -t auth-service:latest .

# Run container
docker-compose up -d
```

## 📊 Service Information
- **Port:** 8001
- **Database:** auth_db
- **Language:** Python 3.11+
- **Framework:** FastAPI

## 📝 License
MIT License
