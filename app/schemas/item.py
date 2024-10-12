from pydantic import BaseModel, RootModel, Field
from datetime import datetime, date
from typing import Optional, List


class ItemBase(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: date


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemInDB(ItemBase):
    id: str = Field(alias="_id")
    insert_date: datetime

    class Config:
        allow_population_by_field_name = True


class AggregatedItemDetail(BaseModel):
    id: str
    name: str
    quantity: int
    expiry_date: Optional[datetime]
    insert_date: Optional[datetime]


class AggregatedItem(BaseModel):
    email: str
    total_items: int
    total_quantity: int
    avg_quantity: float
    min_expiry_date: Optional[datetime]
    max_expiry_date: Optional[datetime]
    expiring_soon: int
    expired: int
    items: List[AggregatedItemDetail]


class AggregationResult(RootModel):
    root: List[AggregatedItem]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
