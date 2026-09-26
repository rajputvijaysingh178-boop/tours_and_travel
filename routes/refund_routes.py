from fastapi import APIRouter, HTTPException
from schemas.refund_schema import RefundCreateSchema
from schemas.refund_schema import RefundCreateSchema

from services.refund_service import (
    create_refund,
    get_refund
)


router = APIRouter(
    prefix="/bookings",
    tags=["Refund"]
)


@router.post("/{booking_id}/refund")
def create_refund_route(
    booking_id: str,
    data: RefundCreateSchema
):
    try:
        return create_refund(
            booking_id,
            data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/{booking_id}/refund")
def get_refund_route(
    booking_id: str
):
    try:
        return get_refund(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
