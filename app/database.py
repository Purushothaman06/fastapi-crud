"""Database module

This module contains functions to connect and disconnect from a MongoDB
database using the Motor library.

"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings


class Database(object):
    """
    A simple class to hold the database connection and instance.

    Attributes:
        client: The AsyncIOMotorClient instance.
        db: The AsyncIOMotorDatabase instance.
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo() -> None:
    """Connect to the MongoDB database

    This function connects to the MongoDB database using the MONGODB_URI
    environment variable and sets the database instance to the specified
    DATABASE_NAME.

    If the connection fails, this function will raise an exception.

    """
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client[settings.DATABASE_NAME]
    await db.client.server_info()


async def close_mongo_connection() -> None:
    """
    Close the connection to the MongoDB database.

    This function closes the connection to the MongoDB database and
    releases any resources held by the connection.

    If the connection is already closed, this function does nothing.

    """
    if db.client:
        db.client.close()


def get_database() -> AsyncIOMotorDatabase:
    """Get the AsyncIOMotorDatabase instance.

    This function returns the AsyncIOMotorDatabase instance which is
    connected to the MongoDB database.

    The database instance is set by connect_to_mongo() and is closed by
    close_mongo_connection().

    Returns:
        The AsyncIOMotorDatabase instance.
    """
    return db.db
