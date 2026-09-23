from fastapi import APIRouter
router = APIRouter(prefix="/bookings", tags=["Invoice"])
@router.get("/{booking_id}/invoice")
def get_invoice(booking_id: str):
    pass