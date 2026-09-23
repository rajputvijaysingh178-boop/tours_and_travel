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