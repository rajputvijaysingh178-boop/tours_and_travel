from fastapi import APIRouter

router = APIRouter(prefix="/bookings",tags=["refund"])
@router.post("/{booking_id}/refund")
def create_refund(booking_id:str):
    pass
@router.get("/{booking_id}/refund")
def get_refund(booking_id:str):
    pass
