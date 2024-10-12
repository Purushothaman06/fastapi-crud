from fastapi import APIRouter, HTTPException
from app.schemas.item import ItemCreate, ItemInDB, ItemUpdate, AggregationResult
from app.services.item_service import ItemService

router = APIRouter()


@router.post("/", response_model=ItemInDB)
async def create_item(item: ItemCreate):
    return await ItemService.create_item(item)


@router.get("/", response_model=list[ItemInDB])
async def filter_items(
    email: str = None,
    expiry_date: str = None,
    insert_date: str = None,
    quantity: int = None,
):
    return await ItemService.filter_items(email, expiry_date, insert_date, quantity)


@router.get("/aggregate", response_model=AggregationResult)
async def aggregate_items():
    try:
        result = await ItemService.aggregate_items()
        return AggregationResult(root=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=ItemInDB)
async def get_item(item_id: str):
    item = await ItemService.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    deleted = await ItemService.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@router.put("/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: ItemUpdate):
    updated_item = await ItemService.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item
