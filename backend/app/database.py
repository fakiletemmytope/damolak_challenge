import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import database_url

logger = logging.getLogger(__name__)

DATABASE_URL = database_url
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set or is empty")
    raise ValueError("DATABASE_URL is not set")

# Log a masked version of the URL for debugging
try:
    masked_url = DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL
    logger.info(f"Connecting to database at: ...@{masked_url}")
    engine = create_async_engine(DATABASE_URL, echo=True)
except Exception as e:
    logger.error(f"Failed to create engine with URL: {DATABASE_URL}")
    raise e


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

        
async def init_db():
    retries = 5
    while retries > 0:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database initialized successfully")
            break
        except Exception as e:
            retries -= 1
            logger.warning(f"Database connection failed. Retrying... ({retries} retries left). Error: {e}")
            if retries == 0:
                logger.error("Could not connect to the database after several retries")
                raise e
            await asyncio.sleep(5)
