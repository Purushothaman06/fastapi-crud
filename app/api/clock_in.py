from fastapi import APIRouter, HTTPException
from app.schemas.clock_in import ClockInCreate, ClockInInDB, ClockInUpdate
from app.services.clock_in_service import ClockInService

router = APIRouter()


@router.post("/", response_model=ClockInInDB)
async def create_clock_in(clock_in: ClockInCreate):
    return await ClockInService.create_clock_in(clock_in)


@router.get("/{clock_in_id}", response_model=ClockInInDB)
async def get_clock_in(clock_in_id: str):
    clock_in = await ClockInService.get_clock_in(clock_in_id)
    if not clock_in:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return clock_in


@router.get("/", response_model=list[ClockInInDB])
async def filter_clock_in(
    email: str = None, location: str = None, insert_datetime: str = None
):
    return await ClockInService.filter_clock_in(email, location, insert_datetime)


@router.delete("/{clock_in_id}")
async def delete_clock_in(clock_in_id: str):
    deleted = await ClockInService.delete_clock_in(clock_in_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return {"message": "Clock-in record deleted successfully"}


@router.put("/{clock_in_id}", response_model=ClockInInDB)
async def update_clock_in(clock_in_id: str, clock_in: ClockInUpdate):
    updated_clock_in = await ClockInService.update_clock_in(clock_in_id, clock_in)
    if not updated_clock_in:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return updated_clock_in
