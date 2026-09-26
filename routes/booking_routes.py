from fastapi import APIRouter, HTTPException, Depends

from services.aut_dependency import get_current_user

from services.booking_service import (
    create_booking,
    get_bookings,
    get_booking,
    confirm_booking,
    cancel_booking)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"])


@router.post("")
def create_booking_route(
    departure_id: str,
    passenger_count: int,
    current_user: dict = Depends(get_current_user)):
    try:
        return create_booking(
            current_user["id"],
            departure_id,
            passenger_count)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e))


@router.get("")
def get_bookings_route(
    current_user: dict = Depends(get_current_user)):
    return get_bookings(current_user["id"])


@router.get("/{booking_id}")
def get_booking_route(booking_id: str):
    try:
        return get_booking(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e))


@router.patch("/{booking_id}/confirm")
def confirm_booking_route(booking_id: str):
    try:
        return confirm_booking(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e))


@router.post("/{booking_id}/cancel")
def cancel_booking_route(
    booking_id: str,
    reason: str
):
    try:
        return cancel_booking(booking_id, reason)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )