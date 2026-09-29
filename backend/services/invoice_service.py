from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import invoices_collection, bookings_collection


def get_invoice(booking_id: str):

    # Validate booking ID
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID") from None

    # Find booking
    booking = bookings_collection.find_one({
        "_id": object_id
    })

    if not booking:
        raise ValueError("Booking not found")

    # Find existing invoice
    invoice = invoices_collection.find_one({
        "booking_id": booking_id
    })

    # Create invoice if it doesn't exist
    if not invoice:

        invoice = {
            "booking_id": booking_id,
            "invoice_number": "INV-" + booking_id,
            "amount": booking["total_amount"],
            "generated_at": datetime.now(
                timezone.utc
            ).replace(tzinfo=None),
            "status": "generated"
        }

        result = invoices_collection.insert_one(invoice)

        invoice["invoice_id"] = str(result.inserted_id)

    else:
        invoice["invoice_id"] = str(invoice["_id"])

    return {
        "invoice_id": invoice["invoice_id"],
        "booking_id": invoice["booking_id"],
        "invoice_number": invoice["invoice_number"],
        "amount": invoice["amount"],
        "generated_at": invoice["generated_at"],
        "status": invoice["status"]
    }