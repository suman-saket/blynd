from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.config import settings

client: AsyncMongoClient | None = None


async def init_db() -> None:
    """Open Mongo and register Beanie document models."""
    global client
    client = AsyncMongoClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB],
        document_models=[],  # add identity/profile Documents later
    )


async def close_db() -> None:
    if client is not None:
        await client.close()