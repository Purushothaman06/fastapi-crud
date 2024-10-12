"""
The module containing the ClockInService class, which provides
methods for creating, retrieving, and deleting clock-in records
in the database.

"""

from app.database import get_database

from app.schemas.clock_in import ClockInCreate, ClockInUpdate, ClockInInDB
from app.config import settings
from bson import ObjectId
from datetime import datetime, timezone


class ClockInService(object):
    """
    The ClockInService class provides methods for creating, retrieving, and
    deleting clock-in records in the database.

    Attributes:
        db: The AsyncIOMotorDatabase instance.

    Methods:
        create_clock_in: Creates a new clock-in record in the database.
        get_clock_in: Retrieves a clock-in record from the database by its ID.
        filter_clock_in: Retrieves a list of clock-in records from the database
            based on the provided filters.
        delete_clock_in: Deletes a clock-in record from the database by its ID.
        update_clock_in: Updates a clock-in record in the database by its ID.
    """

    @staticmethod
    async def create_clock_in(clock_in: ClockInCreate) -> ClockInInDB:
        """
        Creates a new clock-in record in the database.

        Args:
            clock_in (ClockInCreate): The new clock-in data.

        Returns:
            ClockInInDB: The created clock-in record, with the generated ID.
        """

        db = get_database()
        new_clock_in = clock_in.dict()
        new_clock_in["insert_datetime"] = datetime.now(timezone.utc)

        result = await db[settings.CLOCK_IN_COLLECTION].insert_one(new_clock_in)
        created_clock_in = await db[settings.CLOCK_IN_COLLECTION].find_one(
            {"_id": result.inserted_id}
        )

        # Convert ObjectId to string before returning
        if created_clock_in:
            created_clock_in["_id"] = str(created_clock_in["_id"])

        return ClockInInDB(**created_clock_in)

    @staticmethod
    async def get_clock_in(clock_in_id: str) -> ClockInInDB:
        """
        Retrieves a clock-in record from the database by its ID.

        Args:
            clock_in_id (str): The ID of the clock-in record to retrieve.

        Returns:
            ClockInInDB: The retrieved clock-in record, or None if not found.
        """
        db = get_database()
        clock_in = await db[settings.CLOCK_IN_COLLECTION].find_one(
            {"_id": ObjectId(clock_in_id)}
        )
        if clock_in:
            clock_in["_id"] = str(clock_in["_id"])
            return ClockInInDB(**clock_in)
        return None

    @staticmethod
    async def filter_clock_in(
        email: str = None, location: str = None, insert_datetime: str = None
    ) -> list[ClockInInDB]:
        """
        Retrieves a list of clock-in records from the database based on the provided filters.

        Args:
            email (str): Filter by email.
            location (str): Filter by location.
            insert_datetime (str): Filter by insert datetime, in the format "YYYY-MM-DD HH:MM:SS".

        Returns:
            list[ClockInInDB]: The list of filtered clock-in records.
        """

        db = get_database()
        filter_query = {}
        if email:
            filter_query["email"] = email
        if location:
            filter_query["location"] = location
        if insert_datetime:
            filter_query["insert_datetime"] = {
                "$gte": datetime.strptime(insert_datetime, "%Y-%m-%d %H:%M:%S")
            }

        clock_ins = (
            await db[settings.CLOCK_IN_COLLECTION].find(filter_query).to_list(None)
        )

        # Convert ObjectId to string for each clock-in
        return [
            ClockInInDB(**{**clock_in, "_id": str(clock_in["_id"])})
            for clock_in in clock_ins
        ]

    @staticmethod
    async def delete_clock_in(clock_in_id: str) -> bool:
        """
        Deletes a clock-in record from the database by its ID.

        Args:
            clock_in_id (str): The ID of the clock-in record to delete.

        Returns:
            bool: True if the clock-in record was deleted, False otherwise.
        """

        db = get_database()
        result = await db[settings.CLOCK_IN_COLLECTION].delete_one(
            {"_id": ObjectId(clock_in_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    async def update_clock_in(clock_in_id: str, clock_in: ClockInUpdate) -> ClockInInDB:
        """
        Updates a clock-in record in the database by its ID.

        Args:
            clock_in_id (str): The ID of the clock-in record to update.
            clock_in (ClockInUpdate): The updated clock-in data.

        Returns:
            ClockInInDB: The updated clock-in record, or None if the record was not found.
        """

        db = get_database()
        updated_clock_in = clock_in.dict(exclude_unset=True)
        result = await db[settings.CLOCK_IN_COLLECTION].update_one(
            {"_id": ObjectId(clock_in_id)}, {"$set": updated_clock_in}
        )
        if result.modified_count > 0:
            updated_doc = await db[settings.CLOCK_IN_COLLECTION].find_one(
                {"_id": ObjectId(clock_in_id)}
            )
            if updated_doc:
                updated_doc["_id"] = str(updated_doc["_id"])
            return ClockInInDB(**updated_doc)
        return None
