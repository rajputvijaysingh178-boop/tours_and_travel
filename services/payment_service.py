from datetime import datetime, timezone
from bson import ObjectId

from database import payments_collection, bookings_collection


def create_payment(
    booking_id: str,
    payment_data
):
    booking = bookings_collection.find_one({
        "_id": ObjectId(booking_id)
    })

    if not booking:
        raise ValueError("Booking not found")

    payment = {
        "booking_id": booking_id,
        "payment_reference": payment_data.payment_reference,
        "amount": payment_data.amount,
        "status": "completed",
        "payment_date": datetime.now(
            timezone.utc
        ).replace(tzinfo=None)
    }

    result = payments_collection.insert_one(payment)

    bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "payment_status": "paid"
            }
        }
    )

    return {
        "payment_id": str(result.inserted_id),
        "message": "Payment created successfully"
    }


def get_payments(booking_id: str):
    payments = payments_collection.find({
        "booking_id": booking_id
    })

    result = []

    for payment in payments:
        result.append({
            "payment_id": str(payment["_id"]),
            "booking_id": payment["booking_id"],
            "payment_reference": payment["payment_reference"],
            "amount": payment["amount"],
            "status": payment["status"],
            "payment_date": payment["payment_date"]
        })

    return result