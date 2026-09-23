from fastapi import APIRouter
router = APIRouter(prefix="/bookings", tags=["Passengers"])
@router.post("/{booking_id}/passengers")
def add_passenger(booking_id: str):
    pass
@router.get("/{booking_id}/passengers")
def get_passengers(booking_id: str):
    pass
