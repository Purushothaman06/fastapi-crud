from pydantic import BaseModel, Field
from datetime import datetime


class ClockInBase(BaseModel):
    email: str
    location: str


class ClockInCreate(ClockInBase):
    pass


class ClockInUpdate(ClockInBase):
    pass


class ClockInInDB(ClockInBase):
    id: str = Field(alias="_id")
    insert_datetime: datetime

    class Config:
        allow_population_by_field_name = True
