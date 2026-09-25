from fastapi import APIRouter, HTTPException

from schemas.hotel_schema import (
    HotelCreateSchema,
    HotelResponseSchema,
    HotelRoomCreateSchema,
    HotelRoomResponseSchema
)

from services.hotel_service import (
    create_hotel,
    get_hotels,
    add_room,
    get_availability
)

from services.hotel_allocation import allocate_hotel_room


router = APIRouter(
    tags=["Hotels"]
)


@router.post(
    "/hotels",
    response_model=dict
)
def create_hotel_route(
    data: HotelCreateSchema
):
    return create_hotel(data)


@router.get(
    "/hotels",
    response_model=list[HotelResponseSchema]
)
def get_hotels_route():
    return get_hotels()


@router.post(
    "/hotels/{hotel_id}/rooms",
    response_model=dict
)
def add_room_route(
    hotel_id: str,
    data: HotelRoomCreateSchema
):
    try:
        return add_room(hotel_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/hotels/{hotel_id}/availability",
    response_model=list[HotelRoomResponseSchema]
)
def get_availability_route(
    hotel_id: str
):
    try:
        return get_availability(hotel_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
    "/bookings/{booking_id}/hotel-allocation"
)
def allocate_hotel_route(
    booking_id: str,
    hotel_id: str,
    room_id: str
):
    try:
        return allocate_hotel_room(
            booking_id,
            hotel_id,
            room_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )