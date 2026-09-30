from fastapi import APIRouter, Depends, HTTPException

from schemas.invoice_schema import InvoiceResponseSchema
from services.invoice_service import get_invoice
from services.aut_dependency import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=["Invoice"]
)


@router.get(
    "/{booking_id}/invoice",
    response_model=InvoiceResponseSchema
)
def get_invoice_route(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_invoice(booking_id, current_user["id"])
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )