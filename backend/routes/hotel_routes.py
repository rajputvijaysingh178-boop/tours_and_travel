from fastapi import APIRouter, Depends, HTTPException

from schemas.hotel_schema import (
    HotelCreateSchema,
    HotelRoomCreateSchema,
)

from services.hotel_service import (
    create_hotel,
    get_hotels,
    add_room,
    get_availability,
)
from services.aut_dependency import get_admin_user


router = APIRouter(
    tags=["Hotels"]
)


@router.post("/hotels", dependencies=[Depends(get_admin_user)])
def create_hotel_route(
    data: HotelCreateSchema
):
    try:
        return create_hotel(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/hotels")
def get_hotels_route(destination_id: str | None = None):
    return get_hotels(destination_id)


@router.post("/hotels/{hotel_id}/rooms", dependencies=[Depends(get_admin_user)])
def add_room_route(
    hotel_id: str,
    data: HotelRoomCreateSchema,
):
    try:
        return add_room(
            hotel_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/hotels/{hotel_id}/availability"
)
def get_availability_route(
    hotel_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
):
    try:
        return get_availability(
            hotel_id,
            start_date,
            end_date,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )