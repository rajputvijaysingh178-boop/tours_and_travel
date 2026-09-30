from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import refunds_collection, bookings_collection, payments_collection


def _payment_for_booking(booking_id: str, booking: dict):
    payment_id = booking.get("payment_id")
    if payment_id:
        try:
            payment = payments_collection.find_one({
                "_id": ObjectId(str(payment_id)),
            })
            if payment:
                return payment
        except (InvalidId, TypeError):
            pass

    return payments_collection.find_one({
        "booking_id": booking_id,
    })


def _record_refund_request(
    booking_id: str,
    booking: dict,
    payment: dict,
    refund_amount: float,
    refund_percentage: float,
    reason: str,
):
    existing = refunds_collection.find_one({
        "booking_id": booking_id,
        "status": "pending",
    })
    if existing:
        return {
            "refund_id": str(existing["_id"]),
            "status": "pending",
            "message": "Refund is pending provider processing",
        }

    refund = {
        "booking_id": booking_id,
        "payment_id": str(payment["_id"]),
        "refund_amount": refund_amount,
        "refund_percentage": refund_percentage,
        "reason": reason,
        "status": "pending",
        "refund_date": datetime.now(
            timezone.utc
        ).replace(tzinfo=None),
    }
    result = refunds_collection.insert_one(refund)
    bookings_collection.update_one(
        {"_id": booking["_id"]},
        {"$set": {"payment_status": "refund_pending"}},
    )

    return {
        "refund_id": str(result.inserted_id),
        "status": "pending",
        "message": "Refund is pending provider processing",
    }


def request_refund_for_booking(
    booking_id: str,
    booking: dict,
    reason: str,
):
    payment = _payment_for_booking(booking_id, booking)
    if not payment:
        bookings_collection.update_one(
            {"_id": booking["_id"]},
            {"$set": {"payment_status": "refund_pending"}},
        )
        return {
            "refund_id": None,
            "status": "pending",
            "message": "Refund pending; payment record unavailable",
        }

    amount = booking.get("total_amount", booking.get("amount", 0))
    return _record_refund_request(
        booking_id,
        booking,
        payment,
        amount,
        100,
        reason,
    )


def create_refund(booking_id: str, refund_data):
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID") from None

    booking = bookings_collection.find_one({"_id": object_id})
    if not booking:
        raise ValueError("Booking not found")

    payment = _payment_for_booking(booking_id, booking)
    if not payment:
        raise ValueError("Payment not found")

    return _record_refund_request(
        booking_id,
        booking,
        payment,
        refund_data.refund_amount,
        refund_data.refund_percentage,
        refund_data.reason,
    )


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