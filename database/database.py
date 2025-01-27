import logging
from contextlib import asynccontextmanager
from typing import Optional

import asyncpg
from pydantic import PostgresDsn

from settings.base import BackendBaseSettings as base

# Configure logging
logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(self):
        """Initialize the database connection pool."""
        # Construct the database URL
        self.postgres_uri = (
            f"{base.DB_POSTGRES_SCHEMA}://{base.DB_POSTGRES_USERNAME}:{base.DB_POSTGRES_PASSWORD}@"
            f"{base.DB_POSTGRES_HOST}:{base.DB_POSTGRES_PORT}/{base.DB_POSTGRES_NAME}?sslmode=require"
        )

        # Validate the URL using Pydantic
        self.postgres_uri = str(PostgresDsn(self.postgres_uri))
        self._pool: Optional[asyncpg.Pool] = None

    async def initialize(self):
        """Initialize the connection pool."""
        if not self._pool:
            try:
                self._pool = await asyncpg.create_pool(
                    str(self.postgres_uri),
                    min_size=2,
                    max_size=base.DB_POOL_SIZE,
                    max_inactive_connection_lifetime=300.0,
                    server_settings={
                        "application_name": "RAG",
                        "client_encoding": "utf8",
                    },
                )
                if not self._pool:
                    raise Exception("Failed to create connection pool")
                logger.info("Database connection pool initialized successfully.")
            except Exception as e:
                logger.error(f"Error initializing database pool: {str(e)}")
                logger.error(f"Connection URI: {self.postgres_uri}")
                raise

    async def close(self):
        """Close all pool connections."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("Database connection pool closed.")

    @asynccontextmanager
    async def connection(self):
        """Get a connection from the pool."""
        if not self._pool:
            await self.initialize()

        try:
            async with self._pool.acquire() as connection:
                yield connection
        except Exception as e:
            logger.error(f"Error acquiring connection from pool: {str(e)}")
            raise

    @asynccontextmanager
    async def transaction(self):
        """Get a connection and start a transaction."""
        async with self.connection() as connection:
            try:
                async with connection.transaction():
                    yield connection
            except Exception as e:
                logger.error(f"Error in transaction: {str(e)}")
                raise


# Create a singleton instance
async_db = AsyncDatabase()


async def test_connection():
    """Test the database connection."""
    try:
        async with async_db.connection() as conn:
            result = await conn.fetchval("SELECT 1")
            logger.info(f"Connection test successful: {result}")
            return True
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False

async def get_db_connection():
    """Dependency to get a database connection."""
    async with async_db.connection() as conn:
        yield conn