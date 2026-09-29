from database import bookings_collection, hotel_rooms_collection
from bson import ObjectId


def allocate_hotel_room(
    booking_id,
    hotel_id,
    room_id
):
    booking = bookings_collection.find_one(
        {"_id": ObjectId(booking_id)}
    )

    if not booking:
        raise ValueError("Booking not found")

    room = hotel_rooms_collection.find_one(
        {
            "_id": ObjectId(room_id),
            "hotel_id": hotel_id
        }
    )

    if not room:
        raise ValueError("Room not found")

    if room.get("allocated", False):
        raise ValueError("Room is already allocated")

    hotel_rooms_collection.update_one(
        {"_id": ObjectId(room_id)},
        {
            "$set": {
                "allocated": True,
                "booking_id": booking_id
            }
        }
    )

    return {
        "booking_id": booking_id,
        "hotel_id": hotel_id,
        "room_id": room_id,
        "status": "allocated"
    }