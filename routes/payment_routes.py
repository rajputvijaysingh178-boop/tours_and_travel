from fastapi import APIRouter
router = APIRouter(prefix="/bookings", tags=["Payments"])
@router.post("/{booking_id}/payments")
def create_payment(booking_id: str):
    pass
@router.get("/{booking_id}/payments")
def get_payments(booking_id: str):
    pass
