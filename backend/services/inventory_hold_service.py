from datetime import date, datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from config import settings
from database import (
    bookings_collection,
    departures_collection,
    get_client,
    inventory_holds_collection,
    hotel_rooms_collection,
    guides_collection,
    packages_collection,
    vehicles_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise ValueError("Invalid ID")


def _now():
    return datetime.now(timezone.utc)


def _stay(start: str, end: str) -> list[str]:
    try:
        first = date.fromisoformat(start)
        last = date.fromisoformat(end)
    except (TypeError, ValueError):
        raise ValueError("Room availability dates must use YYYY-MM-DD")
    if first.isoformat() != start or last.isoformat() != end or last < first:
        raise ValueError("Invalid trip date range")
    if last == first:
        last += timedelta(days=1)
    return [
        (first + timedelta(days=offset)).isoformat()
        for offset in range((last - first).days)
    ]


def _inventory_end(start: str, end: str) -> str:
    nights = _stay(start, end)
    return (
        (date.fromisoformat(start) + timedelta(days=1)).isoformat()
        if len(nights) == 1 and start == end
        else end
    )


def _booking_dates(booking: dict) -> tuple[str | None, str | None]:
    start = booking.get("travel_date")
    departure = None
    if booking.get("departure_id") and (not start or not booking.get("end_date")):
        try:
            departure = departures_collection.find_one(
                {"_id": ObjectId(str(booking["departure_id"]))}
            )
        except (InvalidId, TypeError):
            pass
    start = start or (departure or {}).get("start_date")
    end = booking.get("end_date") or (departure or {}).get("end_date")
    if start and end == start:
        try:
            end = (date.fromisoformat(start) + timedelta(days=1)).isoformat()
        except (TypeError, ValueError):
            return start, None

    if not end and booking.get("package_id") and start:
        try:
            package = packages_collection.find_one(
                {"_id": ObjectId(str(booking["package_id"]))}
            )
            nights = max(int((package or {}).get("duration", 2)) - 1, 1)
            end = (date.fromisoformat(start) + timedelta(days=nights)).isoformat()
        except (InvalidId, TypeError, ValueError):
            pass
    if not end and start:
        try:
            end = (date.fromisoformat(start) + timedelta(days=1)).isoformat()
        except (TypeError, ValueError):
            pass
    return start, end


def _room_availability(
    room_id: str,
    total_units: int,
    start_date: str,
    end_date: str,
    exclude_cart_id: str | None = None,
    session=None,
) -> int:
    end_date = _inventory_end(start_date, end_date)
    nights = _stay(start_date, end_date)
    if isinstance(total_units, bool) or not isinstance(total_units, int):
        raise ValueError("Room inventory must be a whole number")

    room_ids = [room_id]
    try:
        room_ids.append(ObjectId(room_id))
    except (InvalidId, TypeError):
        pass

    booked = []
    for booking in bookings_collection.find(
        {
            "room_id": {"$in": room_ids},
            "booking_status": {"$nin": ["cancelled", "CANCELLED"]},
        },
        session=session,
    ):
        start, end = _booking_dates(booking)
        if not start or not end or not (start < end_date and start_date < end):
            continue
        quantity = booking.get("room_quantity", 1)
        quantity = quantity if isinstance(quantity, int) and not isinstance(quantity, bool) and quantity > 0 else 1
        booked.append((start, end, quantity))

    hold_query = {
        "resource_type": "hotel_room",
        "resource_id": room_id,
        "status": "active",
        "expires_at": {"$gt": _now()},
    }
    if exclude_cart_id:
        hold_query["cart_id"] = {"$ne": exclude_cart_id}
    held = []
    for hold in inventory_holds_collection.find(hold_query, session=session):
        start = hold.get("start_date") or hold.get("travel_date")
        end = hold.get("end_date")
        if not end and start:
            try:
                end = (date.fromisoformat(start) + timedelta(days=1)).isoformat()
            except (TypeError, ValueError):
                continue
        if not start or not end or not (start < end_date and start_date < end):
            continue
        quantity = hold.get("quantity", 1)
        quantity = quantity if isinstance(quantity, int) and not isinstance(quantity, bool) and quantity > 0 else 1
        held.append((start, end, quantity))

    remaining = []
    for night in nights:
        used = sum(qty for start, end, qty in booked + held if start <= night < end)
        remaining.append(total_units - used)
    return max(0, min(remaining))


def available_room_quantity(room: dict, start_date: str, end_date: str) -> int:
    current = hotel_rooms_collection.find_one({"_id": room["_id"]})
    if not current:
        raise ValueError("Room not found")
    return _room_availability(
        str(current["_id"]),
        current.get("total_units", 0),
        start_date,
        end_date,
    )


def _locked_room(room_id: str, session) -> dict:
    room = hotel_rooms_collection.find_one_and_update(
        {"_id": _object_id(room_id), "status": "active"},
        {"$inc": {"inventory_revision": 1}},
        return_document=ReturnDocument.AFTER,
        session=session,
    )
    if not room:
        raise ValueError("Room is not active")
    return room


def _reserve_room_hold(
    cart_id: str,
    room_id: str,
    start_date: str,
    end_date: str,
    quantity: int,
) -> dict:
    end_date = _inventory_end(start_date, end_date)
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Room quantity must be a positive whole number")

    now = _now()
    hold = {
        "_id": ObjectId(),
        "cart_id": cart_id,
        "resource_type": "hotel_room",
        "resource_id": room_id,
        "travel_date": start_date,
        "start_date": start_date,
        "end_date": end_date,
        "quantity": quantity,
        "status": "active",
        "created_at": now,
        "expires_at": now + timedelta(minutes=settings.HOLD_TTL_MINUTES),
    }

    def reserve(session):
        room = _locked_room(room_id, session)
        if _room_availability(
            room_id,
            room.get("total_units", 0),
            start_date,
            end_date,
            exclude_cart_id=cart_id,
            session=session,
        ) < quantity:
            raise ValueError("Not enough rooms are available for the selected dates")

        inventory_holds_collection.update_many(
            {
                "cart_id": cart_id,
                "resource_type": "hotel_room",
                "status": "active",
            },
            {"$set": {"status": "released", "released_at": now}},
            session=session,
        )
        inventory_holds_collection.insert_one(hold, session=session)
        return hold

    with get_client().start_session() as session:
        saved = session.with_transaction(reserve)
    return {
        "hold_id": str(saved["_id"]),
        "status": "active",
        "expires_at": saved["expires_at"],
        "quantity": quantity,
        "message": "Room inventory held successfully",
    }


def check_resource_exists(resource_type: str, resource_id: str):
    collections = {
        "hotel_room": hotel_rooms_collection,
        "guide": guides_collection,
        "vehicle": vehicles_collection,
    }
    collection = collections.get(resource_type)
    if collection is None:
        raise ValueError("Invalid resource type")
    resource = collection.find_one({"_id": _object_id(resource_id)})
    if not resource:
        raise ValueError(f"{resource_type} not found")
    if resource.get("status") != "active":
        raise ValueError(f"{resource_type} is not active")
    return resource


def create_hold(
    cart_id: str,
    resource_type: str,
    resource_id: str,
    travel_date: str,
    end_date: str | None = None,
    quantity: int = 1,
):
    if resource_type == "hotel_room":
        end_date = end_date or (
            date.fromisoformat(travel_date) + timedelta(days=1)
        ).isoformat()
        return _reserve_room_hold(
            cart_id, resource_id, travel_date, end_date, quantity
        )

    check_resource_exists(resource_type, resource_id)
    query = {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "travel_date": travel_date,
        "status": "active",
        "expires_at": {"$gt": _now()},
    }
    existing = inventory_holds_collection.find_one(query)
    if existing:
        if existing.get("cart_id") == cart_id:
            return {
                "hold_id": str(existing["_id"]),
                "status": "active",
                "expires_at": existing["expires_at"],
                "message": "Hold already exists",
            }
        raise ValueError(f"{resource_type} is currently held")

    hold = {
        "cart_id": cart_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "travel_date": travel_date,
        "status": "active",
        "created_at": _now(),
        "expires_at": _now() + timedelta(minutes=settings.HOLD_TTL_MINUTES),
    }
    result = inventory_holds_collection.insert_one(hold)
    return {
        "hold_id": str(result.inserted_id),
        "status": "active",
        "expires_at": hold["expires_at"],
        "message": "Inventory held successfully",
    }


def validate_cart_room_hold(cart: dict) -> dict | None:
    room_id, quantity = cart.get("room_id"), cart.get("room_quantity")
    if not room_id:
        if quantity is not None:
            raise ValueError("Room quantity cannot be set without a selected room")
        return None
    if quantity is None:  # Existing carts may retain a legacy single-room selection.
        return None
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("Room quantity must be a positive whole number")

    room = check_resource_exists("hotel_room", room_id)
    if str(room.get("hotel_id")) != str(cart.get("hotel_id")):
        raise ValueError("Room does not belong to the selected hotel")
    capacity = room.get("capacity", 0)
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
        raise ValueError("Room capacity must be greater than zero")
    passengers = cart.get("passenger_count", 0)
    minimum = (passengers + capacity - 1) // capacity
    if quantity < minimum:
        raise ValueError(f"At least {minimum} rooms are required for {passengers} passengers")

    hold = inventory_holds_collection.find_one(
        {
            "_id": _object_id(cart.get("room_hold_id", "")),
            "cart_id": str(cart["_id"]),
            "resource_type": "hotel_room",
            "resource_id": room_id,
            "quantity": quantity,
            "start_date": cart.get("travel_date"),
            "end_date": _inventory_end(
                cart.get("travel_date"),
                cart.get("end_date"),
            ),
            "status": "active",
            "expires_at": {"$gt": _now()},
        }
    )
    if not hold:
        raise ValueError("Room inventory hold is missing or expired")
    inventory_end = _inventory_end(cart["travel_date"], cart["end_date"])
    if _room_availability(
        room_id,
        room.get("total_units", 0),
        cart["travel_date"],
        inventory_end,
        exclude_cart_id=str(cart["_id"]),
    ) < quantity:
        raise ValueError("Not enough rooms are available for the selected dates")
    return hold


def extend_cart_holds(cart_id: str, expires_at: datetime) -> None:
    inventory_holds_collection.update_many(
        {
            "cart_id": cart_id,
            "resource_type": "hotel_room",
            "status": "active",
        },
        {"$set": {"expires_at": expires_at, "updated_at": _now()}},
    )


def create_booking_with_room_hold(booking: dict, cart: dict) -> ObjectId:
    room_id, hold_id = cart["room_id"], cart.get("room_hold_id")
    quantity = cart.get("room_quantity")
    if not hold_id or not quantity:
        raise ValueError("Room inventory hold is missing or expired")
    end_date = _inventory_end(cart["travel_date"], cart["end_date"])
    booking_id = ObjectId()

    def convert(session):
        room = _locked_room(room_id, session)
        if str(room.get("hotel_id")) != str(cart.get("hotel_id")):
            raise ValueError("Room does not belong to the selected hotel")
        hold = inventory_holds_collection.find_one(
            {
                "_id": _object_id(hold_id),
                "cart_id": str(cart["_id"]),
                "resource_type": "hotel_room",
                "resource_id": room_id,
                "quantity": quantity,
                "start_date": cart["travel_date"],
                "end_date": end_date,
                "status": "active",
                "expires_at": {"$gt": _now()},
            },
            session=session,
        )
        if not hold:
            raise ValueError("Room inventory hold is missing or expired")

        capacity = room.get("capacity", 0)
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Room capacity must be greater than zero")
        minimum = (cart["passenger_count"] + capacity - 1) // capacity
        if quantity < minimum:
            raise ValueError(f"At least {minimum} rooms are required")
        if _room_availability(
            room_id,
            room.get("total_units", 0),
            cart["travel_date"],
            end_date,
            exclude_cart_id=str(cart["_id"]),
            session=session,
        ) < quantity:
            raise ValueError("Not enough rooms are available for the selected dates")

        booking["_id"] = booking_id
        bookings_collection.insert_one(booking, session=session)
        result = inventory_holds_collection.update_one(
            {
                "_id": hold["_id"],
                "status": "active",
                "expires_at": {"$gt": _now()},
            },
            {
                "$set": {
                    "status": "converted",
                    "booking_id": str(booking_id),
                    "converted_at": _now(),
                }
            },
            session=session,
        )
        if result.modified_count != 1:
            raise ValueError("Room inventory hold is missing or expired")

    with get_client().start_session() as session:
        session.with_transaction(convert)
    return booking_id


def convert_cart_holds(cart_id: str, booking_id: str) -> None:
    inventory_holds_collection.update_many(
        {
            "cart_id": cart_id,
            "resource_type": {"$ne": "hotel_room"},
            "status": "active",
        },
        {
            "$set": {
                "status": "converted",
                "booking_id": booking_id,
                "converted_at": _now(),
            }
        },
    )


def get_cart_holds(cart_id: str):
    holds = inventory_holds_collection.find(
        {
            "cart_id": cart_id,
            "status": "active",
            "expires_at": {"$gt": _now()},
        }
    )
    return [
        {
            "hold_id": str(hold["_id"]),
            "resource_type": hold["resource_type"],
            "resource_id": hold["resource_id"],
            "travel_date": hold["travel_date"],
            "start_date": hold.get("start_date"),
            "end_date": hold.get("end_date"),
            "quantity": hold.get("quantity", 1),
            "status": hold["status"],
            "expires_at": hold["expires_at"],
        }
        for hold in holds
    ]


def release_hold(hold_id: str):
    result = inventory_holds_collection.update_one(
        {"_id": _object_id(hold_id), "status": "active"},
        {"$set": {"status": "released", "released_at": _now()}},
    )
    if not result.matched_count:
        raise ValueError("Active inventory hold not found")
    return {"hold_id": hold_id, "status": "released"}


def release_cart_room_holds(cart_id: str) -> dict:
    result = inventory_holds_collection.update_many(
        {
            "cart_id": cart_id,
            "resource_type": "hotel_room",
            "status": "active",
        },
        {"$set": {"status": "released", "released_at": _now()}},
    )
    return {"cart_id": cart_id, "released_count": result.modified_count}


def release_booking_room_hold(booking: dict) -> None:
    hold_id = booking.get("room_hold_id")
    if not hold_id:
        return
    inventory_holds_collection.update_one(
        {
            "_id": _object_id(hold_id),
            "booking_id": str(booking["_id"]),
            "resource_type": "hotel_room",
            "status": "converted",
        },
        {"$set": {"status": "released", "released_at": _now()}},
    )


def release_cart_holds(cart_id: str):
    result = inventory_holds_collection.update_many(
        {"cart_id": cart_id, "status": "active"},
        {"$set": {"status": "released", "released_at": _now()}},
    )
    return {"cart_id": cart_id, "released_count": result.modified_count}


def expire_old_holds():
    result = inventory_holds_collection.update_many(
        {"status": "active", "expires_at": {"$lte": _now()}},
        {"$set": {"status": "expired", "expired_at": _now()}},
    )
    return {"expired_count": result.modified_count}
