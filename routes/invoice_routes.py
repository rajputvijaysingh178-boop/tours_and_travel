from fastapi import APIRouter, HTTPException

from schemas.invoice_schema import InvoiceResponseSchema
from services.invoice_service import get_invoice


router = APIRouter(
    prefix="/bookings",
    tags=["Invoice"]
)


@router.get(
    "/{booking_id}/invoice",
    response_model=InvoiceResponseSchema
)
def get_invoice_route(
    booking_id: str
):
    try:
        return get_invoice(booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )