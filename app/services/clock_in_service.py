from app.database import get_database
from app.schemas.clock_in import ClockInCreate, ClockInUpdate, ClockInInDB
from app.config import settings
from bson import ObjectId
from datetime import datetime, timezone


class ClockInService:
    @staticmethod
    async def create_clock_in(clock_in: ClockInCreate) -> ClockInInDB:
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
        db = get_database()
        clock_in = await db[settings.CLOCK_IN_COLLECTION].find_one(
            {"_id": ObjectId(clock_in_id)}
        )
        if clock_in:
            clock_in["_id"] = str(clock_in["_id"])  # Convert ObjectId to string
            return ClockInInDB(**clock_in)
        return None

    @staticmethod
    async def filter_clock_in(
        email: str = None, location: str = None, insert_datetime: str = None
    ) -> list[ClockInInDB]:
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
        db = get_database()
        result = await db[settings.CLOCK_IN_COLLECTION].delete_one(
            {"_id": ObjectId(clock_in_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    async def update_clock_in(clock_in_id: str, clock_in: ClockInUpdate) -> ClockInInDB:
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
                updated_doc["_id"] = str(
                    updated_doc["_id"]
                )  # Convert ObjectId to string
            return ClockInInDB(**updated_doc)
        return None
