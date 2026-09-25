<<<<<<< HEAD
from fastapi import APIRouter
router = APIRouter(prefix="/bookings", tags=["Passengers"])
@router.post("/{booking_id}/passengers")
def add_passenger(booking_id: str):
    pass
@router.get("/{booking_id}/passengers")
def get_passengers(booking_id: str):
    pass
=======
from fastapi import APIRouter, HTTPException

from schemas.passenger_schema import PassengerCreateSchema
from services.passanger_service import (
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
>>>>>>> origin/anil
