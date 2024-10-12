from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings


class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client[settings.DATABASE_NAME]
    await db.client.server_info()  # This will raise an exception if the connection fails


async def close_mongo_connection():
    if db.client:
        db.client.close()


def get_database() -> AsyncIOMotorDatabase:
    return db.db
