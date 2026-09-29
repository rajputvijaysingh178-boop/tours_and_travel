from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    trip_carts_collection,
    payment_orders_collection,
)

from services.pricing_service import calculate_cart_price


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _now():
    return datetime.now(timezone.utc)


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

    if cart.get("status") != "reviewing":
        raise ValueError(
            "Cart must be reviewed before payment"
        )

    if not cart.get("review_confirmed"):
        raise ValueError(
            "Review must be confirmed"
        )

    if len(cart.get("passengers", [])) != cart.get(
        "passenger_count"
    ):
        raise ValueError(
            "Passenger details are incomplete"
        )

    # Recalculate price on server
    price = calculate_cart_price(cart)

    amount = price["grand_total"]

    # Lock cart
    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "status": "locked_for_payment",
                "price_snapshot": price,
                "updated_at": _now(),
            }
        }
    )

    order = {
        "cart_id": cart_id,
        "customer_id": customer_id,
        "amount": amount,
        "currency": "INR",
        "status": "created",
        "provider": "razorpay",
        "provider_order_id": None,
        "created_at": _now(),
        "updated_at": _now(),
    }

    result = payment_orders_collection.insert_one(order)

    return {
        "payment_order_id": str(result.inserted_id),
        "cart_id": cart_id,
        "amount": amount,
        "currency": "INR",
        "status": "created",
        "message": "Payment order created successfully",
    }


def get_payment_order(
    payment_order_id: str,
    customer_id: str,
):
    order = payment_orders_collection.find_one({
        "_id": _object_id(payment_order_id),
        "customer_id": customer_id,
    })

    if not order:
        raise ValueError(
            "Payment order not found"
        )

    return {
        "payment_order_id": str(order["_id"]),
        "cart_id": order["cart_id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "status": order["status"],
        "provider": order["provider"],
        "provider_order_id": order.get(
            "provider_order_id"
        ),
        "created_at": order["created_at"],
        "updated_at": order["updated_at"],
    }