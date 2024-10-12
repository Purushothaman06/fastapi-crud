"""Endpoints for clock-in records.

This module contains the endpoints for creating, retrieving, and deleting
clock-in records in the database.

"""

from fastapi import APIRouter, HTTPException
from app.schemas.clock_in import ClockInCreate, ClockInInDB, ClockInUpdate
from app.services.clock_in_service import ClockInService

router = APIRouter()


@router.post("/", response_model=ClockInInDB)
async def create_clock_in(new_clock_in: ClockInCreate) -> ClockInInDB:
    """Create a new clock-in record"""
    return await ClockInService.create_clock_in(new_clock_in)


@router.get("/{clock_in_id}", response_model=ClockInInDB)
async def get_clock_in_by_id(clock_in_id: str) -> ClockInInDB:
    """Get a clock-in record by its ID"""

    clock_in = await ClockInService.get_clock_in(clock_in_id)

    if not clock_in:
        raise HTTPException(status_code=404, detail="Clock-in record not found")

    return clock_in


@router.get("/", response_model=list[ClockInInDB])
async def read_clock_ins(
    email_filter: str | None = None,
    location_filter: str | None = None,
    insert_datetime_filter: str | None = None,
) -> list[ClockInInDB]:
    """
    Retrieve a list of clock-in records from the database based on optional filters.
    """
    return await ClockInService.filter_clock_ins(
        email_filter=email_filter,
        location_filter=location_filter,
        insert_datetime_filter=insert_datetime_filter,
    )


@router.delete("/{clock_in_id}", response_model=dict[str, str])
async def delete_clock_in(clock_in_id: str) -> dict[str, str]:
    """
    Delete a clock-in record by its ID
    """
    deleted = await ClockInService.delete_clock_in(clock_in_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Clock-in record not found")
    return {"message": "Clock-in record deleted successfully"}


@router.put("/{clock_in_id}", response_model=ClockInInDB)
async def update_clock_in_by_id(
    clock_in_id: str, updated_clock_in_data: ClockInUpdate
) -> ClockInInDB:
    """Update a clock-in record by its ID"""

    updated_clock_in = await ClockInService.update_clock_in(
        clock_in_id, updated_clock_in_data
    )

    if not updated_clock_in:
        raise HTTPException(status_code=404, detail="Clock-in record not found in this id")

    return updated_clock_in
