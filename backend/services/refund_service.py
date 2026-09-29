from datetime import datetime, timezone
from bson import ObjectId

from database import refunds_collection, bookings_collection, payments_collection


def create_refund(booking_id: str, refund_data):
    booking = bookings_collection.find_one({
        "_id": ObjectId(booking_id)
    })

    if not booking:
        raise ValueError("Booking not found")

    payment = payments_collection.find_one({
        "booking_id": booking_id,
        "status": "completed"
    })

    if not payment:
        raise ValueError("Payment not found")

    refund = {
        "booking_id": booking_id,
        "payment_id": str(payment["_id"]),
        "refund_amount": refund_data.refund_amount,
        "refund_percentage": refund_data.refund_percentage,
        "reason": refund_data.reason,
        "status": "processed",
        "refund_date": datetime.now(
            timezone.utc
        ).replace(tzinfo=None)
    }

    result = refunds_collection.insert_one(refund)

    bookings_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "payment_status": "refunded"
            }
        }
    )

    return {
        "refund_id": str(result.inserted_id),
        "message": "Refund processed successfully"
    }


def get_refund(booking_id: str):
    refund = refunds_collection.find_one({
        "booking_id": booking_id
    })

    if not refund:
        raise ValueError("Refund not found")

    return {
        "refund_id": str(refund["_id"]),
        "booking_id": refund["booking_id"],
        "payment_id": refund["payment_id"],
        "refund_amount": refund["refund_amount"],
        "refund_percentage": refund["refund_percentage"],
        "reason": refund["reason"],
        "status": refund["status"],
        "refund_date": refund["refund_date"]
    }