"""Endpoints for items.

This module contains the endpoints for creating, retrieving, filtering, aggregating,
and retrieving individual items in the database.

"""

from fastapi import APIRouter, HTTPException
from app.schemas.item import ItemCreate, ItemInDB, ItemUpdate, AggregationResult
from app.services.item_service import ItemService

router = APIRouter()


@router.post("/", response_model=ItemInDB)
async def create_item(new_item: ItemCreate) -> ItemInDB:
    """Creates a new item in the database."""
    return await ItemService.create_item(new_item)


@router.get("/", response_model=list[ItemInDB])
async def read_items(
    email: str | None = None,
    expiry_date: str | None = None,
    insert_date: str | None = None,
    quantity: int | None = None,
) -> list[ItemInDB]:
    """Retrieves a list of items from the database based on the provided filters."""
    return await ItemService.filter_items(
        email=email,
        expiry_date=expiry_date,
        insert_date=insert_date,
        quantity=quantity,
    )


@router.get("/aggregate", response_model=AggregationResult)
async def read_aggregated_items() -> AggregationResult:
    """Returns the aggregated items from the database."""
    try:
        aggregated_items = await ItemService.aggregate_items()
        return AggregationResult(root=aggregated_items)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error aggregating items") from e


@router.get("/{item_id}", response_model=ItemInDB)
async def read_item_by_id(item_id: str) -> ItemInDB:
    """Retrieves an item from the database by its ID."""
    item = await ItemService.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in this item_id")
    return item


@router.delete("/{item_id}", response_model=dict[str, str])
async def delete_item_by_id(item_id: str) -> dict[str, str]:
    """Deletes an item from the database by its ID."""
    deleted = await ItemService.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@router.put("/{item_id}", response_model=ItemInDB)
async def update_item_by_id(item_id: str, updated_item_data: ItemUpdate) -> ItemInDB:
    """Updates an item in the database by its ID."""

    updated_item = await ItemService.update_item(item_id, updated_item_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found in this item_id")

    return updated_item
