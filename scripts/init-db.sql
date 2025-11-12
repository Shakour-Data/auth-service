-- Initialize Auth Service Database
-- This script runs automatically when PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE auth_service TO gravity;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Auth Service database initialized successfully!';
    RAISE NOTICE 'Database: auth_service';
    RAISE NOTICE 'User: gravity';
    RAISE NOTICE 'Extensions: uuid-ossp, pg_trgm';
END $$;
