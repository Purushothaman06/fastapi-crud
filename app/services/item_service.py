"""Services for items.

This module contains a class (`ItemService`) which provides methods
for creating, retrieving, filtering, aggregating, deleting, and updating
items in the database.

"""

from app.database import get_database
from app.schemas.item import ItemCreate, ItemUpdate, ItemInDB
from app.config import settings
from bson import ObjectId
from datetime import datetime, timezone, date


class ItemService(object):
    """
    Service class for items.

    This class provides methods for creating, retrieving, filtering, aggregating, deleting, and updating items in the database.

    Attributes:
        db (motor.motor_asyncio.AsyncIOMotorDatabase): The database object.
    """

    @staticmethod
    async def create_item(item: ItemCreate) -> ItemInDB:
        """
        Creates a new item in the database.

        Args:
            item (ItemCreate): The new item data.

        Returns:
            ItemInDB: The created item, with the generated ID.
        """
        db = get_database()
        new_item = item.dict()

        # Convert `expiry_date` from date to datetime, if it exists
        if "expiry_date" in new_item and isinstance(new_item["expiry_date"], date):
            new_item["expiry_date"] = datetime.combine(
                new_item["expiry_date"], datetime.min.time()
            )

        new_item["insert_date"] = datetime.now(timezone.utc)
        result = await db[settings.ITEMS_COLLECTION].insert_one(new_item)
        created_item = await db[settings.ITEMS_COLLECTION].find_one(
            {"_id": result.inserted_id}
        )

        # Convert ObjectId to string for the ItemInDB model
        created_item["_id"] = str(created_item["_id"])
        return ItemInDB(**created_item)

    @staticmethod
    async def get_item(item_id: str) -> ItemInDB:
        """
        Retrieves an item from the database by its ID.

        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            ItemInDB: The retrieved item, or None if not found.
        """

        db = get_database()
        item = await db[settings.ITEMS_COLLECTION].find_one({"_id": ObjectId(item_id)})
        if item:
            # Convert ObjectId to string for the ItemInDB model
            item["_id"] = str(item["_id"])
            return ItemInDB(**item)
        return None

    @staticmethod
    async def filter_items(
        email: str = None,
        expiry_date: str = None,
        insert_date: str = None,
        quantity: int = None,
    ) -> list[ItemInDB]:
        """
        Filter items based on email, expiry date, insert date, and quantity.

        Args:
            email (str): Filter by email.
            expiry_date (str): Filter by expiry date, in the format "YYYY-MM-DD".
            insert_date (str): Filter by insert date, in the format "YYYY-MM-DD".
            quantity (int): Filter by quantity.

        Returns:
            list[ItemInDB]: A list of filtered items.
        """
        db = get_database()
        filter_query = {}
        if email:
            filter_query["email"] = email
        if expiry_date:
            expiry_datetime = datetime.combine(
                datetime.strptime(expiry_date, "%Y-%m-%d").date(), datetime.min.time()
            )
            filter_query["expiry_date"] = {"$gte": expiry_datetime}
        if insert_date:
            filter_query["insert_date"] = {
                "$gte": datetime.strptime(insert_date, "%Y-%m-%d")
            }

        if quantity is not None:
            filter_query["quantity"] = {"$gte": quantity}

        items = await db[settings.ITEMS_COLLECTION].find(filter_query).to_list(None)

        # Convert ObjectId to string for each item in the list
        return [ItemInDB(**{**item, "_id": str(item["_id"])}) for item in items]

    @staticmethod
    async def aggregate_items() -> list[any]:
        """
        Aggregate items to return the count of items for each email, total quantity, average quantity, minimum and maximum expiry dates, and the count of items that are expiring soon (in the next 7 days) and expired.

        Returns:
            list[any]: A list of aggregated items
        """

        db = get_database()
        now = datetime.now(timezone.utc)
        pipeline = [
            {
                "$group": {
                    "_id": "$email",
                    "total_items": {"$sum": 1},
                    "total_quantity": {"$sum": "$quantity"},
                    "avg_quantity": {"$avg": "$quantity"},
                    "min_expiry_date": {"$min": "$expiry_date"},
                    "max_expiry_date": {"$max": "$expiry_date"},
                    "items": {
                        "$push": {
                            "id": "$_id",
                            "name": "$name",
                            "quantity": "$quantity",
                            "expiry_date": "$expiry_date",
                            "insert_date": "$insert_date",
                        }
                    },
                }
            },
            {
                "$project": {
                    "email": "$_id",
                    "total_items": 1,
                    "total_quantity": 1,
                    "avg_quantity": {"$round": ["$avg_quantity", 2]},
                    "min_expiry_date": 1,
                    "max_expiry_date": 1,
                    "expiring_soon": {
                        "$size": {
                            "$filter": {
                                "input": "$items",
                                "as": "item",
                                "cond": {
                                    "$and": [
                                        {"$gte": ["$$item.expiry_date", now]},
                                        {
                                            "$lte": [
                                                "$$item.expiry_date",
                                                {
                                                    "$add": [
                                                        now,
                                                        7 * 24 * 60 * 60 * 1000,
                                                    ]
                                                },
                                            ]
                                        },
                                    ]
                                },
                            }
                        }
                    },
                    "expired": {
                        "$size": {
                            "$filter": {
                                "input": "$items",
                                "as": "item",
                                "cond": {"$lt": ["$$item.expiry_date", now]},
                            }
                        }
                    },
                    "items": 1,
                }
            },
            {"$sort": {"total_quantity": -1}},
        ]

        result = await db[settings.ITEMS_COLLECTION].aggregate(pipeline).to_list(None)

        # Convert ObjectId to string and format dates
        for item in result:
            item["email"] = str(item["_id"])
            del item["_id"]
            item["min_expiry_date"] = (
                item["min_expiry_date"].isoformat() if item["min_expiry_date"] else None
            )
            item["max_expiry_date"] = (
                item["max_expiry_date"].isoformat() if item["max_expiry_date"] else None
            )
            for subitem in item["items"]:
                subitem["id"] = str(subitem["id"])
                subitem["expiry_date"] = (
                    subitem["expiry_date"].isoformat()
                    if subitem["expiry_date"]
                    else None
                )
                subitem["insert_date"] = (
                    subitem["insert_date"].isoformat()
                    if subitem["insert_date"]
                    else None
                )

        return result

    @staticmethod
    async def delete_item(item_id: str) -> bool:
        """
        Deletes an item from the database.

        Args:
            item_id (str): The ID of the item to delete.

        Returns:
            bool: True if the item was deleted, False otherwise.
        """

        db = get_database()
        result = await db[settings.ITEMS_COLLECTION].delete_one(
            {"_id": ObjectId(item_id)}
        )
        return result.deleted_count > 0

    @staticmethod
    async def update_item(item_id: str, item: ItemUpdate) -> ItemInDB:
        """
        Updates an item in the database.

        Args:
            item_id (str): The ID of the item to update.
            item (ItemUpdate): The updated item data.

        Returns:
            ItemInDB: The updated item, or None if the item was not found.
        """

        db = get_database()
        updated_item = item.dict(exclude_unset=True)

        # Convert `expiry_date` from date to datetime, if it exists
        if "expiry_date" in updated_item and isinstance(
            updated_item["expiry_date"], date
        ):
            updated_item["expiry_date"] = datetime.combine(
                updated_item["expiry_date"], datetime.min.time()
            )

        result = await db[settings.ITEMS_COLLECTION].update_one(
            {"_id": ObjectId(item_id)}, {"$set": updated_item}
        )
        if result.modified_count > 0:
            updated_doc = await db[settings.ITEMS_COLLECTION].find_one(
                {"_id": ObjectId(item_id)}
            )
            # Convert ObjectId to string for the ItemInDB model
            updated_doc["_id"] = str(updated_doc["_id"])
            return ItemInDB(**updated_doc)
        return None
