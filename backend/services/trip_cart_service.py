from datetime import datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId

from config import settings
from database import (
    trip_carts_collection,
    packages_collection,
    hotels_collection,
    hotel_rooms_collection,
    activities_collection,
    guides_collection,
    vehicles_collection,
)

from services.pricing_service import calculate_cart_price
from services.inventory_hold_service import (
    create_hold,
    release_cart_holds,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _now():
    return datetime.now(timezone.utc)


def _serialize(cart):
    return {
        "cart_id": str(cart["_id"]),
        "customer_id": cart["customer_id"],
        "package_id": cart["package_id"],
        "destination_id": cart.get("destination_id"),
        "travel_date": cart["travel_date"],
        "passenger_count": cart["passenger_count"],
        "nights": cart.get("nights", 1),
        "hotel_id": cart.get("hotel_id"),
        "room_id": cart.get("room_id"),
        "activity_ids": cart.get("activity_ids", []),
        "guide_id": cart.get("guide_id"),
        "vehicle_id": cart.get("vehicle_id"),
        "passengers": cart.get("passengers", []),
        "status": cart.get("status", "draft"),
        "review_confirmed": cart.get(
            "review_confirmed",
            False
        ),
        "price_snapshot": cart.get(
            "price_snapshot"
        ),
        "expires_at": cart.get("expires_at"),
        "created_at": cart.get("created_at"),
        "updated_at": cart.get("updated_at"),
    }


def create_trip_cart(
    customer_id: str,
    data
):
    if data.passenger_count > 5:
        raise ValueError(
            "Maximum 5 passengers allowed"
        )

    package = packages_collection.find_one({
        "_id": _object_id(data.package_id)
    })

    if not package:
        raise ValueError("Package not found")

    if package.get("status") == "deleted":
        raise ValueError("Package is not available")

    max_passengers = package.get(
        "max_passengers",
        5
    )

    if data.passenger_count > max_passengers:
        raise ValueError(
            f"Maximum {max_passengers} passengers "
            "allowed for this package"
        )

    now = _now()

    cart = {
        "customer_id": customer_id,
        "package_id": data.package_id,
        "destination_id": package.get(
            "destination_id"
        ),
        "travel_date": data.travel_date,
        "passenger_count": data.passenger_count,
        "nights": max(
            package.get("duration", 1) - 1,
            1
        ),
        "hotel_id": None,
        "room_id": None,
        "activity_ids": [],
        "guide_id": None,
        "vehicle_id": None,
        "passengers": [],
        "status": "draft",
        "review_confirmed": False,
        "price_snapshot": None,
        "created_at": now,
        "updated_at": now,
        "expires_at": now + timedelta(
            minutes=settings.CART_TTL_MINUTES
        ),
    }

    result = trip_carts_collection.insert_one(cart)

    cart["_id"] = result.inserted_id

    price = calculate_cart_price(cart)

    trip_carts_collection.update_one(
        {"_id": result.inserted_id},
        {
            "$set": {
                "price_snapshot": price,
                "updated_at": _now(),
            }
        }
    )

    cart["price_snapshot"] = price

    return _serialize(cart)


def get_trip_cart(
    cart_id: str,
    customer_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    if cart.get("status") in [
        "converted",
        "abandoned",
        "expired",
    ]:
        return _serialize(cart)

    if cart.get("expires_at") and (
        cart["expires_at"] <= _now()
    ):
        trip_carts_collection.update_one(
            {"_id": cart["_id"]},
            {
                "$set": {
                    "status": "expired",
                    "updated_at": _now(),
                }
            }
        )

        release_cart_holds(cart_id)

        cart["status"] = "expired"

        return _serialize(cart)

    price = calculate_cart_price(cart)

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "price_snapshot": price,
                "updated_at": _now(),
            }
        }
    )

    cart["price_snapshot"] = price

    return _serialize(cart)


def _ensure_draft(cart):
    if cart.get("status") != "draft":
        raise ValueError(
            "Cart can no longer be modified"
        )


def update_trip_cart(
    cart_id: str,
    customer_id: str,
    update_data: dict
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                **update_data,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def select_hotel(
    cart_id: str,
    customer_id: str,
    hotel_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    hotel = hotels_collection.find_one({
        "_id": _object_id(hotel_id)
    })

    if not hotel:
        raise ValueError("Hotel not found")

    if hotel.get("status") != "active":
        raise ValueError("Hotel is not active")

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "hotel_id": hotel_id,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def select_room(
    cart_id: str,
    customer_id: str,
    room_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    room = hotel_rooms_collection.find_one({
        "_id": _object_id(room_id)
    })

    if not room:
        raise ValueError("Room not found")

    if room.get("status") != "active":
        raise ValueError("Room is not active")

    if (
        cart.get("hotel_id")
        and str(room.get("hotel_id"))
        != str(cart["hotel_id"])
    ):
        raise ValueError(
            "Room does not belong to selected hotel"
        )

    create_hold(
        cart_id,
        "hotel_room",
        room_id,
        cart["travel_date"],
    )

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "room_id": room_id,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def select_activities(
    cart_id: str,
    customer_id: str,
    activity_ids: list[str]
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    for activity_id in activity_ids:
        activity = activities_collection.find_one({
            "_id": _object_id(activity_id)
        })

        if not activity:
            raise ValueError(
                f"Activity {activity_id} not found"
            )

        if activity.get("status") != "active":
            raise ValueError(
                f"Activity {activity_id} is not active"
            )

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "activity_ids": activity_ids,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def select_guide(
    cart_id: str,
    customer_id: str,
    guide_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    guide = guides_collection.find_one({
        "_id": _object_id(guide_id)
    })

    if not guide:
        raise ValueError("Guide not found")

    if guide.get("status") != "active":
        raise ValueError("Guide is not active")

    create_hold(
        cart_id,
        "guide",
        guide_id,
        cart["travel_date"],
    )

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "guide_id": guide_id,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def select_vehicle(
    cart_id: str,
    customer_id: str,
    vehicle_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    vehicle = vehicles_collection.find_one({
        "_id": _object_id(vehicle_id)
    })

    if not vehicle:
        raise ValueError("Vehicle not found")

    if vehicle.get("status") != "active":
        raise ValueError(
            "Vehicle is not active"
        )

    if vehicle.get("capacity", 0) < cart[
        "passenger_count"
    ]:
        raise ValueError(
            "Vehicle capacity is too small"
        )

    create_hold(
        cart_id,
        "vehicle",
        vehicle_id,
        cart["travel_date"],
    )

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "vehicle_id": vehicle_id,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def confirm_review(
    cart_id: str,
    customer_id: str
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    price = calculate_cart_price(cart)

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "status": "reviewing",
                "review_confirmed": True,
                "price_snapshot": price,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )


def add_passengers(
    cart_id: str,
    customer_id: str,
    passengers: list
):
    cart = trip_carts_collection.find_one({
        "_id": _object_id(cart_id),
        "customer_id": customer_id,
    })

    if not cart:
        raise ValueError("Trip cart not found")

    _ensure_draft(cart)

    if len(passengers) != cart[
        "passenger_count"
    ]:
        raise ValueError(
            f"Exactly {cart['passenger_count']} "
            "passenger details are required"
        )

    if len(passengers) > 5:
        raise ValueError(
            "Maximum 5 passengers allowed"
        )

    passenger_data = [
        passenger.model_dump()
        if hasattr(passenger, "model_dump")
        else passenger
        for passenger in passengers
    ]

    trip_carts_collection.update_one(
        {"_id": cart["_id"]},
        {
            "$set": {
                "passengers": passenger_data,
                "updated_at": _now(),
            }
        }
    )

    return get_trip_cart(
        cart_id,
        customer_id
    )