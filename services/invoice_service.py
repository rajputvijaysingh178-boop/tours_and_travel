from datetime import datetime, timezone

from database import invoices_collection, bookings_collection


def get_invoice(booking_id: str):
    booking = bookings_collection.find_one({
        "_id": booking_id
    })

    invoice = invoices_collection.find_one({
        "booking_id": booking_id
    })

    if not invoice:
        if not booking:
            raise ValueError("Booking not found")

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