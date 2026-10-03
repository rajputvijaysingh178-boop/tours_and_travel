from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    bookings_collection,
    departures_collection,
    packages_collection,
    destinations_collection,
    customers_collection,
    users_collection,
    passengers_collection,
    payments_collection,
    invoices_collection,
    hotels_collection,
    hotel_rooms_collection,
    vehicles_collection,
    guides_collection,
    transport_assignments_collection,
)
from services.inventory_hold_service import (
    release_cart_holds,
    release_booking_room_hold,
)
from services.package_service import validate_package_travel_date
from services.refund_service import request_refund_for_booking


def _find_reference(collection, value):
    if not value:
        return None

    try:
        return collection.find_one({"_id": ObjectId(str(value))})
    except (InvalidId, TypeError):
        return None


def _public_document(document):
    if not document:
        return None

    def normalize(value):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, dict):
            return {
                key: normalize(item)
                for key, item in value.items()
                if key != "_id"
            }
        if isinstance(value, list):
            return [normalize(item) for item in value]
        return value

    return normalize({
        key: value
        for key, value in document.items()
        if key != "_id"
    })


def _booking_summary(booking):
    package = _find_reference(
        packages_collection,
        booking.get("package_id"),
    )
    destination = _find_reference(
        destinations_collection,
        booking.get("destination_id")
        or (package or {}).get("destination_id"),
    )
    departure = _find_reference(
        departures_collection,
        booking.get("departure_id"),
    )
    booking_id = str(booking["_id"])
    payment = _find_reference(
        payments_collection,
        booking.get("payment_id"),
    )
    if not payment:
        payment = payments_collection.find_one({"booking_id": booking_id})

    passenger_count = booking.get("passenger_count")
    if passenger_count is None:
        embedded_passengers = booking.get("passengers") or []
        passenger_count = len(embedded_passengers) or len(list(
            passengers_collection.find({"booking_id": booking_id})
        ))

    result = {
        key: value
        for key, value in booking.items()
        if key != "_id"
    }
    result.update({
        "booking_id": booking_id,
        "package_name": (package or {}).get("name"),
        "destination": (
            (destination or {}).get("name")
            or (package or {}).get("destination")
        ),
        "destination_state": (destination or {}).get("state"),
        "travel_date": (
            booking.get("travel_date")
            or (departure or {}).get("start_date")
            or (package or {}).get("start_date")
        ),
        "end_date": (
            booking.get("end_date")
            or (departure or {}).get("end_date")
            or (package or {}).get("end_date")
        ),
        "total_amount": booking.get(
            "total_amount",
            booking.get("amount"),
        ),
        "passenger_count": passenger_count,
        "payment_status": (
            booking.get("payment_status")
            or (payment or {}).get("status")
        ),
    })
    return result


def _booking_details(booking, customer_id):
    result = _booking_summary(booking)
    package = _find_reference(
        packages_collection,
        booking.get("package_id"),
    )
    destination = _find_reference(
        destinations_collection,
        booking.get("destination_id")
        or (package or {}).get("destination_id"),
    )
    customer = customers_collection.find_one({"user_id": customer_id})
    user = _find_reference(users_collection, customer_id)

    stored_passengers = list(passengers_collection.find({
        "booking_id": result["booking_id"],
    }))
    passenger_details = booking.get("passengers") or stored_passengers

    payment = _find_reference(
        payments_collection,
        booking.get("payment_id"),
    )
    if not payment:
        payment = payments_collection.find_one({
            "booking_id": result["booking_id"],
        })
    invoice = invoices_collection.find_one({
        "booking_id": result["booking_id"],
    })

    hotel = _find_reference(hotels_collection, booking.get("hotel_id"))
    room = _find_reference(hotel_rooms_collection, booking.get("room_id"))
    vehicle = _find_reference(vehicles_collection, booking.get("vehicle_id"))
    guide = _find_reference(guides_collection, booking.get("guide_id"))
    transport = transport_assignments_collection.find_one({
        "booking_id": result["booking_id"],
    })
    if not transport and booking.get("departure_id"):
        transport = transport_assignments_collection.find_one({
            "departure_id": booking["departure_id"],
        })
    if not vehicle and transport:
        vehicle = _find_reference(vehicles_collection, transport.get("vehicle_id"))

    result.update({
        "package": {
            "package_id": str(package["_id"]),
            "name": package.get("name"),
        } if package else None,
        "destination_details": {
            "destination_id": str(destination["_id"]),
            "name": destination.get("name"),
            "state": destination.get("state"),
            "country": destination.get("country"),
        } if destination else None,
        "customer": {
            "name": (user or {}).get("name"),
            "email": (user or {}).get("email"),
            "phone": (customer or {}).get("phone"),
            "address": (customer or {}).get("address"),
        },
        "passengers": [
            _public_document(passenger)
            for passenger in passenger_details
        ],
        "passenger_count": booking.get(
            "passenger_count",
            len(passenger_details),
        ),
        "hotel": _public_document(hotel),
        "room": _public_document(room),
        "vehicle": _public_document(vehicle),
        "guide": _public_document(guide),
        "transport": _public_document(transport),
        "payment": {
            "payment_id": str(payment["_id"]),
            "status": payment.get("status"),
            "amount": payment.get("amount"),
            "payment_date": payment.get("payment_date")
            or payment.get("created_at"),
            "payment_reference": payment.get("payment_reference"),
        } if payment else None,
        "invoice": {
            "invoice_id": str(invoice["_id"]),
            "invoice_number": invoice.get("invoice_number"),
            "amount": invoice.get("amount"),
            "status": invoice.get("status"),
            "generated_at": invoice.get("generated_at")
            or invoice.get("created_at"),
        } if invoice else None,
    })
    return result


def create_booking(
    customer_id: str,
    package_id: str,
    travel_date: str,
    passenger_count: int
):
    if passenger_count <= 0:
        raise ValueError("Passenger count must be greater than 0")

    if not travel_date:
        raise ValueError("Travel date is required")

    # Validate package ID
    try:
        package_object_id = ObjectId(package_id)
    except InvalidId:
        raise ValueError("Invalid package ID")

    # Find package
    package = packages_collection.find_one({
        "_id": package_object_id
    })

    if not package:
        raise ValueError("Package not found")

    travel_date, end_date = validate_package_travel_date(
        package,
        travel_date,
    )
    max_passengers = package.get("max_passengers", 5)
    if passenger_count > max_passengers:
        raise ValueError(
            f"Maximum {max_passengers} passengers allowed for this package"
        )

    base_price = package.get("base_price", 0)

    total_amount = base_price * passenger_count

    booking = {
        "customer_id": customer_id,
        "package_id": package_id,

        # Customer-selected date
        "travel_date": travel_date,
        "end_date": end_date,

        "passenger_count": passenger_count,
        "total_amount": total_amount,

        "booking_status": "pending",
        "payment_status": "pending",

        "cancellation_details": None,

        "created_at": datetime.now(
            timezone.utc
        ).replace(tzinfo=None)
    }

    result = bookings_collection.insert_one(booking)
    destination = _find_reference(
        destinations_collection,
        package.get("destination_id"),
    )

    return {
        "booking_id": str(result.inserted_id),
        "package_id": package_id,
        "package_name": package.get("name"),
        "destination": (
            (destination or {}).get("name")
            or package.get("destination")
        ),
        "travel_date": travel_date,
        "end_date": end_date,
        "passenger_count": passenger_count,
        "total_amount": total_amount,
        "booking_status": "pending",
        "payment_status": "pending",
        "message": "Booking created successfully"
    }


def get_bookings(customer_id: str):
    bookings = bookings_collection.find({
        "customer_id": customer_id
    })
    return [_booking_summary(booking) for booking in bookings]


def get_booking(booking_id: str, customer_id: str):
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID")

    booking = bookings_collection.find_one({
        "_id": object_id,
        "customer_id": customer_id,
    })

    if not booking:
        raise ValueError("Booking not found")

    return _booking_details(booking, customer_id)


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


def cancel_booking(
    booking_id: str,
    customer_id: str,
    reason: str,
    additional_reason: str | None = None,
):
    try:
        object_id = ObjectId(booking_id)
    except InvalidId:
        raise ValueError("Invalid booking ID")

    booking = bookings_collection.find_one({
        "_id": object_id,
        "customer_id": customer_id,
    })

    if not booking:
        raise ValueError("Booking not found")

    status = str(booking.get("booking_status", "")).lower()
    if status not in {"pending", "confirmed"}:
        raise ValueError("Booking is not eligible for cancellation")

    cancellation_details = {
        "reason": reason,
        "cancelled_at": datetime.now(
            timezone.utc
        ).replace(tzinfo=None)
    }
    if additional_reason:
        cancellation_details["additional_reason"] = additional_reason

    update_result = bookings_collection.update_one(
        {
            "_id": object_id,
            "customer_id": customer_id,
            "booking_status": booking.get("booking_status"),
        },
        {
            "$set": {
                "booking_status": "cancelled",
                "cancellation_details": cancellation_details
            }
        }
    )
    if update_result.matched_count == 0:
        raise ValueError("Booking status changed; refresh and try again")

    if booking.get("cart_id"):
        release_cart_holds(str(booking["cart_id"]))
    release_booking_room_hold(booking)

    payment_status = str(booking.get("payment_status", "")).lower()
    refund = None
    if payment_status in {"paid", "completed", "captured", "success", "successful"}:
        refund_reason = (
            f"{reason}: {additional_reason}"
            if additional_reason
            else reason
        )
        refund = request_refund_for_booking(
            booking_id,
            booking,
            refund_reason,
        )

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking_id,
        "booking_status": "cancelled",
        "payment_status": (
            "refund_pending" if refund else booking.get("payment_status")
        ),
        "refund": refund,
    }