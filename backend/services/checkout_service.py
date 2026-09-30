from datetime import datetime, timezone
import secrets

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    trip_carts_collection,
    payment_orders_collection,
    bookings_collection,
    payments_collection,
    invoices_collection,
    vouchers_collection,
    inventory_holds_collection,
)

from services.pricing_service import calculate_cart_price


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _now():
    return datetime.now(timezone.utc)


def lock_cart(cart_id: str, customer_id: str):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    if cart.get("status") != "reviewing":
        raise ValueError(
            "Cart must be reviewed before checkout"
        )

    if not cart.get("review_confirmed"):
        raise ValueError(
            "Review must be confirmed"
        )

    passenger_count = cart.get(
        "passenger_count",
        0
    )

    passengers = cart.get(
        "passengers",
        []
    )

    if passenger_count < 1 or passenger_count > 5:
        raise ValueError(
            "Passenger count must be between 1 and 5"
        )

    if len(passengers) != passenger_count:
        raise ValueError(
            "Complete passenger details are required"
        )

    price = calculate_cart_price(cart)

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "status": "locked_for_payment",
                "price_snapshot": price,
                "locked_at": _now(),
                "updated_at": _now(),
            }
        }
    )

    return {
        "cart_id": cart_id,
        "status": "locked_for_payment",
        "amount": price["grand_total"],
        "price": price,
    }


def create_payment_order(
    cart_id: str,
    customer_id: str,
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    if cart.get("status") != "locked_for_payment":
        raise ValueError(
            "Cart must be locked before payment"
        )

    price = cart.get("price_snapshot")

    if not price:
        price = calculate_cart_price(cart)

    amount = float(
        price["grand_total"]
    )

    order = {
        "cart_id": cart_id,
        "customer_id": customer_id,
        "amount": amount,
        "currency": "INR",
        "provider": "razorpay",
        "provider_order_id": None,
        "status": "pending",
        "created_at": _now(),
        "updated_at": _now(),
    }

    result = payment_orders_collection.insert_one(
        order
    )

    return {
        "payment_order_id": str(
            result.inserted_id
        ),
        "cart_id": cart_id,
        "amount": amount,
        "currency": "INR",
        "status": "pending",
    }


def verify_payment(
    cart_id: str,
    customer_id: str,
    payment_id: str,
    payment_signature: str | None = None,
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    if cart.get("status") != "locked_for_payment":
        raise ValueError(
            "Cart is not ready for payment verification"
        )

    payment_order = payment_orders_collection.find_one({
        "cart_id": cart_id,
        "customer_id": customer_id,
        "status": "pending",
    })

    if not payment_order:
        raise ValueError(
            "Payment order not found"
        )

    # Temporary verification for development.
    # Real Razorpay signature verification will replace this.
    amount = payment_order["amount"]

    payment = {
        "cart_id": cart_id,
        "customer_id": customer_id,
        "payment_order_id": str(
            payment_order["_id"]
        ),
        "payment_id": payment_id,
        "payment_signature": payment_signature,
        "amount": amount,
        "currency": "INR",
        "status": "paid",
        "created_at": _now(),
    }

    payment_result = payments_collection.insert_one(
        payment
    )

    payment_orders_collection.update_one(
        {"_id": payment_order["_id"]},
        {
            "$set": {
                "status": "verified",
                "provider_payment_id": payment_id,
                "updated_at": _now(),
            }
        }
    )

    # Create booking only AFTER payment verification
    booking = {
        "customer_id": customer_id,
        "cart_id": cart_id,
        "package_id": cart["package_id"],
        "destination_id": cart.get(
            "destination_id"
        ),
        "travel_date": cart["travel_date"],
        "passenger_count": cart[
            "passenger_count"
        ],
        "passengers": cart.get(
            "passengers",
            []
        ),
        "hotel_id": cart.get("hotel_id"),
        "room_id": cart.get("room_id"),
        "activity_ids": cart.get(
            "activity_ids",
            []
        ),
        "guide_id": cart.get("guide_id"),
        "vehicle_id": cart.get(
            "vehicle_id"
        ),
        "amount": amount,
        "booking_status": "CONFIRMED",
        "payment_status": "PAID",
        "payment_id": str(
            payment_result.inserted_id
        ),
        "created_at": _now(),
        "updated_at": _now(),
    }

    booking_result = bookings_collection.insert_one(
        booking
    )

    booking_id = str(
        booking_result.inserted_id
    )

    # Convert active holds to sold
    inventory_holds_collection.update_many(
        {
            "cart_id": cart_id,
            "status": "active",
        },
        {
            "$set": {
                "status": "converted",
                "booking_id": booking_id,
                "converted_at": _now(),
            }
        }
    )

    # Invoice
    invoice_number = (
        f"INV-{secrets.token_hex(4).upper()}"
    )

    invoice = {
        "invoice_number": invoice_number,
        "booking_id": booking_id,
        "customer_id": customer_id,
        "amount": amount,
        "currency": "INR",
        "status": "generated",
        "created_at": _now(),
    }

    invoice_result = invoices_collection.insert_one(
        invoice
    )

    invoice_id = str(
        invoice_result.inserted_id
    )

    # Voucher
    voucher_code = (
        f"TRAVEL-{secrets.token_hex(4).upper()}"
    )

    voucher = {
        "voucher_code": voucher_code,
        "booking_id": booking_id,
        "customer_id": customer_id,
        "travel_date": cart["travel_date"],
        "status": "active",
        "created_at": _now(),
    }

    voucher_result = vouchers_collection.insert_one(
        voucher
    )

    voucher_id = str(
        voucher_result.inserted_id
    )

    # Finish cart
    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "status": "converted",
                "booking_id": booking_id,
                "updated_at": _now(),
            }
        }
    )

    return {
        "cart_id": cart_id,
        "payment_order_id": str(
            payment_order["_id"]
        ),
        "booking_id": booking_id,
        "invoice_id": invoice_id,
        "voucher_id": voucher_id,
        "amount": amount,
        "payment_id": payment_id,
        "status": "CONFIRMED",
        "message": "Payment verified and booking confirmed",
    }