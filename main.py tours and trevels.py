from fastapi import FastAPI, HTTPException
from models import Hotel, HotelRoom
from service import HotelAllocationService

app = FastAPI()

service = HotelAllocationService()


@app.post("/hotels")
def create_hotel(hotel: Hotel):
    return service.create_hotel(hotel)


@app.get("/hotels")
def get_hotels():
    return service.get_hotels()


@app.post("/hotels/{hotel_id}/rooms")
def add_room(hotel_id: int, room: HotelRoom):

    result = service.add_room(hotel_id, room)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )

    return result


@app.get("/hotels/{hotel_id}/availability")
def get_availability(hotel_id: int):

    result = service.get_availability(hotel_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Hotel not found"
        )

    return result


@app.post("/bookings/{booking_id}/hotel-allocation")
def allocate_hotel(
    booking_id: int,
    hotel_id: int,
    room_id: int
):

    result = service.allocate_room(
        booking_id,
        hotel_id,
        room_id
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Room unavailable or hotel not found"
        )

    return result