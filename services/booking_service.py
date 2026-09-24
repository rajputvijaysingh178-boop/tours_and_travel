from datetime import datetime, timezone
from bson import ObjectId

from database import bookings_collection


def create_booking(
    customer_id: str,
    departure_id: str,
    passenger_count: int,
    total_amount: float
):
    booking = {
        "customer_id": customer_id,
        "departure_id": departure_id,
        "passenger_count": passenger_count,
        "total_amount": total_amount,
        "booking_status": "pending",
        "payment_status": "pending",
        "cancellation_details": None,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
    }

    result = bookings_collection.insert_one(booking)

    return {
        "booking_id": str(result.inserted_id),
        "message": "Booking created successfully"
    }


def get_bookings(customer_id: str):
    bookings = bookings_collection.find({
        "customer_id": customer_id
    })

    result = []

    for booking in bookings:
        booking["booking_id"] = str(booking["_id"])
        del booking["_id"]
        result.append(booking)

    return result


def get_booking(booking_id: str):
    booking = bookings_collection.find_one({
        "_id": ObjectId(booking_id)
    })

    if not booking:
        raise ValueError("Booking not found")

    booking["booking_id"] = str(booking["_id"])
    del booking["_id"]

    return booking


def confirm_booking(booking_id: str):
    booking = bookings_collection.find_one({
        "_id": ObjectId(booking_id)
    })

    if not booking:
        raise ValueError("Booking not found")

    bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "booking_status": "confirmed"
            }
        }
    )

    return {
        "message": "Booking confirmed successfully",
        "booking_id": booking_id
    }


def cancel_booking(booking_id: str, reason: str):
    booking = bookings_collection.find_one({
        "_id": ObjectId(booking_id)
    })

    if not booking:
        raise ValueError("Booking not found")

    bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "booking_status": "cancelled",
                "cancellation_details": {
                    "reason": reason,
                    "cancelled_at": datetime.now(
                        timezone.utc
                    ).replace(tzinfo=None)
                }
            }
        }
    )

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking_id
    }