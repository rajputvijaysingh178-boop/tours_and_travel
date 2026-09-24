from fastapi import APIRouter, HTTPException

from schemas.payment_schema import PaymentCreateSchema
from services.payment_service import (
    create_payment,
    get_payments
)


router = APIRouter(
    prefix="/bookings",
    tags=["Payments"]
)


@router.post("/{booking_id}/payments")
def create_payment_route(
    booking_id: str,
    data: PaymentCreateSchema
):
    try:
        return create_payment(
            booking_id,
            data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/{booking_id}/payments")
def get_payments_route(
    booking_id: str
):
    return get_payments(booking_id)