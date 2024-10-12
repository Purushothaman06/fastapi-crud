"""
Schemas for items.

This module contains the Pydantic models used to define the
structure of items in the database and the API.

"""

from pydantic import BaseModel, RootModel, Field
from datetime import datetime, date
from typing import Iterator, Optional


class ItemBase(BaseModel):
    """
    Base model for items.

    This model is used as a base for other item models, such as
    `ItemCreate`, `ItemUpdate`, and `ItemInDB`. It contains the
    essential fields for an item, such as the name, email, item name,
    quantity, and expiry date.

    """

    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: date


class ItemCreate(ItemBase):
    """
    ItemCreate model.

    This model is used to validate the data when creating a new item.
    It is the same as the `ItemBase` model, but with the additional
    constraint that the `expiry_date` field must be a date in the
    future.

    """

    pass


class ItemUpdate(ItemBase):
    """
    ItemUpdate model.

    This model is used to validate the data when updating an item.
    It is the same as the `ItemBase` model, but it allows the fields to
    be optional, because the user may not want to update all of them.

    """

    pass


class ItemInDB(ItemBase):
    """
    ItemInDB model.

    This model is used to represent an item in the database. It
    contains the essential fields for an item, such as the name, email,
    item name, quantity, expiry date, and insert date.

    Attributes:
        id (str): The ID of the item.
        insert_date (datetime): The date and time the item was inserted
            into the database.
    """

    id: str = Field(alias="_id")
    insert_date: datetime

    """
    ItemInDB model configuration.

    This class contains the configuration for the ItemInDB model.

    Attributes:
        allow_population_by_field_name (bool): Whether to allow population
            of the model by field name. Defaults to True.
    """

    class Config(object):
        """
        ItemInDB model configuration.

        This class contains the configuration for the ItemInDB model.

        Attributes:
            allow_population_by_field_name (bool): Whether to allow population
                of the model by field name. Defaults to True.
        """

        allow_population_by_field_name = True


class AggregatedItemDetail(BaseModel):
    """
    An item detail in an aggregated item.

    This model contains the details of a single item in an
    aggregated item. It includes the item ID, name, quantity, expiry
    date, and insert date.
    """

    id: str
    name: str
    quantity: int
    expiry_date: Optional[datetime]
    insert_date: Optional[datetime]


class AggregatedItem(BaseModel):
    """
    An aggregated item.

    This model contains the result of an aggregation query for a
    single item. It includes the count of items for a given email,
    total quantity, average quantity, minimum and maximum expiry
    dates, and the count of items that are expiring soon (in the next
    7 days) and expired.

    """

    email: str
    total_items: int
    total_quantity: int
    avg_quantity: float
    min_expiry_date: Optional[datetime]
    max_expiry_date: Optional[datetime]
    expiring_soon: int
    expired: int
    items: list[AggregatedItemDetail]


class AggregationResult(RootModel):
    """
    The result of an aggregation query.

    This model contains the result of an aggregation query, which
    includes the count of items for each email, total quantity, average
    quantity, minimum and maximum expiry dates, and the count of items
    that are expiring soon (in the next 7 days) and expired.

    Attributes:
        root (list[AggregatedItem]): The list of aggregated items.
    """

    root: list[AggregatedItem]

    def __iter__(self) -> Iterator[AggregatedItem]:
        """
        Iterate over the aggregated items.

        Returns:
            Iterator[AggregatedItem]: An iterator over the aggregated items.
        """
        return iter(self.root)

    def __getitem__(self, item: str) -> AggregatedItem:
        """
        Get an aggregated item by email.

        Args:
            item (str): The email address of the aggregated item to retrieve.

        Returns:
            AggregatedItem: The aggregated item with the given email, or None if not found.
        """
        return self.root[item]
