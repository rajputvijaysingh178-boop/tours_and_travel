from fastapi import APIRouter

from schemas.passenger_schema import PassengerCreateSchema

from services.passenger_service import (
    add_passenger,
    get_passengers
)


router = APIRouter(
    prefix="/bookings",
    tags=["Passengers"]
)


@router.post("/{booking_id}/passengers")
def add_passenger_route(
    booking_id: str,
    data: PassengerCreateSchema
):
    return add_passenger(
        booking_id,
        data
    )


@router.get("/{booking_id}/passengers")
def get_passengers_route(
    booking_id: str
):
    return get_passengers(booking_id)