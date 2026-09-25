<<<<<<< HEAD
from fastapi import APIRouter
router = APIRouter(prefix="/bookings", tags=["Bookings"])
@router.post("")
def create_booking():
    pass

@router.get("")
def get_bookings():
    pass

@router.get("/{booking_id}")
def get_booking(booking_id: str):
    pass

@router.patch("/{booking_id}/confirm")
def confirm_booking(booking_id: str):
    pass

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: str):
    pass
=======
from fastapi import APIRouter, HTTPException

from services.booking_service import (
    create_booking,
    get_bookings,
    get_booking,
    confirm_booking,
    cancel_booking
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post("")
def create_booking_route(
    customer_id: str,
    departure_id: str,
    passenger_count: int,
    total_amount: float
):
    return create_booking(
        customer_id,
        departure_id,
        passenger_count,
        total_amount
    )


@router.get("")
def get_bookings_route(
    customer_id: str
):
    return get_bookings(customer_id)


@router.get("/{booking_id}")
def get_booking_route(
    booking_id: str
):
    try:
        return get_booking(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.patch("/{booking_id}/confirm")
def confirm_booking_route(
    booking_id: str
):
    try:
        return confirm_booking(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post("/{booking_id}/cancel")
def cancel_booking_route(
    booking_id: str,
    reason: str
):
    try:
        return cancel_booking(
            booking_id,
            reason
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
>>>>>>> origin/anil
