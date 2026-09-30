from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from services.aut_dependency import get_current_user

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


class BookingCancellationRequest(BaseModel):
    reason: str
    additional_reason: str | None = None


@router.post("")
def create_booking_route(
    package_id: str,
    travel_date: str,
    passenger_count: int,
    current_user: dict = Depends(get_current_user)
):
    try:
        return create_booking(
            current_user["id"],
            package_id,
            travel_date,
            passenger_count
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_bookings_route(
    current_user: dict = Depends(get_current_user)
):
    return get_bookings(
        current_user["id"]
    )


@router.get("/{booking_id}")
def get_booking_route(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_booking(
            booking_id,
            current_user["id"],
        )

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
        return confirm_booking(
            booking_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post("/{booking_id}/cancel")
def cancel_booking_route(
    booking_id: str,
    cancellation: BookingCancellationRequest | None = None,
    reason: str = "Customer requested cancellation",
    current_user: dict = Depends(get_current_user),
):
    selected_reason = cancellation.reason.strip() if cancellation else reason.strip()
    if not selected_reason:
        raise HTTPException(status_code=422, detail="Cancellation reason is required")
    additional_reason = (
        cancellation.additional_reason.strip() or None
        if cancellation and cancellation.additional_reason
        else None
    )
    try:
        return cancel_booking(
            booking_id,
            current_user["id"],
            selected_reason,
            additional_reason,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )