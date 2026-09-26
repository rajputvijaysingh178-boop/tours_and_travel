from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    bookings_collection,
    departures_collection,
    packages_collection
)


def create_booking(
    customer_id: str,
    departure_id: str,
    passenger_count: int
):
    if passenger_count <= 0:
        raise ValueError("Passenger count must be greater than 0")

    try:
        departure_object_id = ObjectId(departure_id)
    except InvalidId:
        raise ValueError("Invalid departure ID")

    departure = departures_collection.find_one({
        "_id": departure_object_id
    })

    if not departure:
        raise ValueError("Departure not found")

    if departure.get("status") != "scheduled":
        raise ValueError("This departure is not available")

    capacity = departure.get("capacity", 0)

    existing_bookings = bookings_collection.find({
        "departure_id": departure_id,
        "booking_status": {
            "$in": ["pending", "confirmed"]
        }
    })

    booked_passengers = sum(
        booking.get("passenger_count", 0)
        for booking in existing_bookings
    )

    if booked_passengers + passenger_count > capacity:
        raise ValueError("Not enough seats available")

    package_id = departure.get("package_id")

    if not package_id:
        raise ValueError("Package not linked to departure")

    try:
        package_object_id = ObjectId(package_id)
    except InvalidId:
        raise ValueError("Invalid package ID")

    package = packages_collection.find_one({
        "_id": package_object_id
    })

    if not package:
        raise ValueError("Package not found")

    base_price = package.get("base_price", 0)

    total_amount = base_price * passenger_count

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
        "total_amount": total_amount,
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
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID")

    booking = bookings_collection.find_one({
        "_id": object_id
    })

    if not booking:
        raise ValueError("Booking not found")

    booking["booking_id"] = str(booking["_id"])
    del booking["_id"]

    return booking


def confirm_booking(booking_id: str):
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID")

    booking = bookings_collection.find_one({
        "_id": object_id
    })

    if not booking:
        raise ValueError("Booking not found")

    bookings_collection.update_one(
        {"_id": object_id},
        {"$set": {"booking_status": "confirmed"}}
    )

    return {
        "message": "Booking confirmed successfully",
        "booking_id": booking_id
    }


def cancel_booking(booking_id: str, reason: str):
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID")

    booking = bookings_collection.find_one({
        "_id": object_id
    })

    if not booking:
        raise ValueError("Booking not found")

    bookings_collection.update_one(
        {"_id": object_id},
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