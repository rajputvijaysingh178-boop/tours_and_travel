from datetime import datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId

from config import settings
from database import (
    inventory_holds_collection,
    hotel_rooms_collection,
    guides_collection,
    vehicles_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _now():
    return datetime.now(timezone.utc)


def _expires_at():
    return _now() + timedelta(
        minutes=settings.HOLD_TTL_MINUTES
    )


def _active_hold_query(
    resource_type: str,
    resource_id: str,
    travel_date: str,
):
    return {
        "resource_type": resource_type,
        "resource_id": resource_id,
        "travel_date": travel_date,
        "status": "active",
        "expires_at": {
            "$gt": _now()
        },
    }


def check_resource_exists(
    resource_type: str,
    resource_id: str,
):
    collections = {
        "hotel_room": hotel_rooms_collection,
        "guide": guides_collection,
        "vehicle": vehicles_collection,
    }

    collection = collections.get(resource_type)

    if collection is None:
        raise ValueError("Invalid resource type")

    resource = collection.find_one({
        "_id": _object_id(resource_id)
    })

    if not resource:
        raise ValueError(
            f"{resource_type} not found"
        )

    if resource.get("status") != "active":
        raise ValueError(
            f"{resource_type} is not active"
        )

    return resource


def create_hold(
    cart_id: str,
    resource_type: str,
    resource_id: str,
    travel_date: str,
):
    check_resource_exists(
        resource_type,
        resource_id,
    )

    existing_hold = inventory_holds_collection.find_one(
        _active_hold_query(
            resource_type,
            resource_id,
            travel_date,
        )
    )

    if existing_hold:
        if existing_hold.get("cart_id") == cart_id:
            return {
                "hold_id": str(
                    existing_hold["_id"]
                ),
                "status": "active",
                "expires_at": existing_hold[
                    "expires_at"
                ],
                "message": "Hold already exists"
            }

        raise ValueError(
            f"{resource_type} is currently held"
        )

    hold = {
        "cart_id": cart_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "travel_date": travel_date,
        "status": "active",
        "created_at": _now(),
        "expires_at": _expires_at(),
    }

    result = inventory_holds_collection.insert_one(
        hold
    )

    return {
        "hold_id": str(result.inserted_id),
        "status": "active",
        "expires_at": hold["expires_at"],
        "message": "Inventory held successfully"
    }


def get_cart_holds(cart_id: str):
    holds = inventory_holds_collection.find({
        "cart_id": cart_id,
        "status": "active",
        "expires_at": {
            "$gt": _now()
        },
    })

    return [
        {
            "hold_id": str(hold["_id"]),
            "resource_type": hold["resource_type"],
            "resource_id": hold["resource_id"],
            "travel_date": hold["travel_date"],
            "status": hold["status"],
            "expires_at": hold["expires_at"],
        }
        for hold in holds
    ]


def release_hold(hold_id: str):
    result = inventory_holds_collection.update_one(
        {
            "_id": _object_id(hold_id),
            "status": "active",
        },
        {
            "$set": {
                "status": "released",
                "released_at": _now(),
            }
        }
    )

    if result.matched_count == 0:
        raise ValueError("Active hold not found")

    return {
        "hold_id": hold_id,
        "status": "released",
    }


def release_cart_holds(cart_id: str):
    result = inventory_holds_collection.update_many(
        {
            "cart_id": cart_id,
            "status": "active",
        },
        {
            "$set": {
                "status": "released",
                "released_at": _now(),
            }
        }
    )

    return {
        "cart_id": cart_id,
        "released_count": result.modified_count,
    }


def expire_old_holds():
    result = inventory_holds_collection.update_many(
        {
            "status": "active",
            "expires_at": {
                "$lte": _now()
            },
        },
        {
            "$set": {
                "status": "expired",
                "expired_at": _now(),
            }
        }
    )

    return {
        "expired_count": result.modified_count
    }