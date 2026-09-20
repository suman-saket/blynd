from beanie import init_beanie
from pymongo import AsyncMongoClient

from src.core.config import settings
from src.identity.models import OtpChallenge, User

client: AsyncMongoClient | None = None


async def init_db() -> None:
    """Open Mongo and register Beanie document models."""
    global client
    client = AsyncMongoClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB],
        document_models=[User, OtpChallenge],
    )


async def close_db() -> None:
    if client is not None:
        await client.close()
