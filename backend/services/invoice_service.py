from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    invoices_collection,
    bookings_collection,
    packages_collection,
    destinations_collection,
    customers_collection,
    users_collection,
    passengers_collection,
    payments_collection,
)


def get_invoice(booking_id: str, customer_id: str):

    # Validate booking ID
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID") from None

    # Find booking
    booking = bookings_collection.find_one({
        "_id": object_id,
        "customer_id": customer_id,
    })

    if not booking:
        raise ValueError("Booking not found")

    package = None
    if booking.get("package_id"):
        try:
            package = packages_collection.find_one({
                "_id": ObjectId(str(booking["package_id"])),
            })
        except InvalidId:
            package = None

    destination = None
    if package and package.get("destination_id"):
        try:
            destination = destinations_collection.find_one({
                "_id": ObjectId(str(package["destination_id"])),
            })
        except InvalidId:
            destination = None

    customer = customers_collection.find_one({
        "user_id": customer_id,
    })
    user = users_collection.find_one({
        "_id": ObjectId(customer_id),
    })
    passengers = booking.get("passengers") or list(
        passengers_collection.find({
            "booking_id": booking_id,
        })
    )
    payment = None
    if booking.get("payment_id"):
        try:
            payment = payments_collection.find_one({
                "_id": ObjectId(str(booking["payment_id"])),
            })
        except InvalidId:
            payment = None
    if not payment:
        payment = payments_collection.find_one({"booking_id": booking_id})

    # Find existing invoice
    invoice = invoices_collection.find_one({
        "booking_id": booking_id
    })

    # Create invoice if it doesn't exist
    if not invoice:
        booking_amount = booking.get(
            "total_amount",
            booking.get("amount", 0),
        )

        invoice = {
            "booking_id": booking_id,
            "invoice_number": "INV-" + booking_id,
            "amount": booking_amount,
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
        "generated_at": invoice.get("generated_at")
        or invoice.get("created_at"),
        "status": invoice["status"],
        "customer_name": (user or {}).get("name"),
        "package_name": (package or {}).get("name"),
        "passengers": [
            {
                key: value
                for key, value in passenger.items()
                if key not in {"_id", "booking_id"}
            }
            for passenger in passengers
        ],
        "payment_status": (
            booking.get("payment_status")
            or (payment or {}).get("status")
        ),
        "total_amount": booking.get(
            "total_amount",
            booking.get("amount", invoice.get("amount")),
        ),
        "destination": (
            (destination or {}).get("name")
            or (package or {}).get("destination")
        ),
    }