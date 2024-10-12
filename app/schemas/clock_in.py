"""
Schemas for clock-in records.

This module contains the Pydantic models used to define the structure of
clock-in records in the database and the API.

"""

from pydantic import BaseModel, Field
from datetime import datetime


class ClockInBase(BaseModel):
    """
    Base model for clock-in records.

    This model contains the essential fields for a clock-in record,
    such as the email and location.
    """

    email: str
    location: str


class ClockInCreate(ClockInBase):
    """
    Model for creating a new clock-in record.

    This model is used to validate the data when creating a new clock-in
    record. It is the same as the `ClockInBase` model, but it does not
    contain the `id` and `insert_datetime` fields, because these are
    generated automatically by the database.
    """

    pass


class ClockInUpdate(ClockInBase):
    """
    Model for updating an existing clock-in record.

    This model is used to validate the data when updating an existing
    clock-in record. It is the same as the `ClockInBase` model, but it
    allows the fields to be optional, because the user may not want to
    update all of them.

    """

    pass


class ClockInInDB(ClockInBase):
    """
    Model for a clock-in record in the database.

    This model is used to define the structure of a clock-in record in the
    database. It contains the essential fields for a clock-in record, such
    as the email and location, as well as the ID and insert datetime, which
    are generated automatically by the database.
    """

    id: str = Field(alias="_id")
    insert_datetime: datetime

    class Config(object):
        """
        Configuration for the ClockInInDB model.

        This class contains configuration for the ClockInInDB model, such as
        allowing population by field name.

        """

        allow_population_by_field_name = True
