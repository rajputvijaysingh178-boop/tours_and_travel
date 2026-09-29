from bson import ObjectId
from bson.errors import InvalidId

from database import (
    activities_collection,
    destinations_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _serialize(activity: dict):
    return {
        "activity_id": str(activity["_id"]),
        "destination_id": activity.get("destination_id"),
        "name": activity.get("name", ""),
        "description": activity.get("description", ""),
        "duration_minutes": activity.get("duration_minutes", 0),
        "price": activity.get("price", 0),
        "price_unit": activity.get("price_unit", "per_person"),
        "images": activity.get("images", []),
        "status": activity.get("status", "active"),
    }


def create_activity(data):
    destination = destinations_collection.find_one({
        "_id": _object_id(data.destination_id)
    })

    if not destination:
        raise ValueError("Destination not found")

    if data.price_unit not in ["per_person", "per_group"]:
        raise ValueError(
            "price_unit must be per_person or per_group"
        )

    activity = {
        "destination_id": data.destination_id,
        "name": data.name,
        "description": data.description,
        "duration_minutes": data.duration_minutes,
        "price": data.price,
        "price_unit": data.price_unit,
        "images": data.images,
        "status": data.status,
    }

    result = activities_collection.insert_one(activity)

    return {
        "activity_id": str(result.inserted_id),
        "message": "Activity created successfully"
    }


def get_activities(destination_id=None):
    query = {
        "status": {"$ne": "deleted"}
    }

    if destination_id:
        query["destination_id"] = destination_id

    activities = activities_collection.find(query)

    return [
        _serialize(activity)
        for activity in activities
    ]


def get_activity(activity_id: str):
    activity = activities_collection.find_one({
        "_id": _object_id(activity_id)
    })

    if not activity:
        raise ValueError("Activity not found")

    return _serialize(activity)


def update_activity(activity_id: str, data):
    object_id = _object_id(activity_id)

    activity = activities_collection.find_one({
        "_id": object_id
    })

    if not activity:
        raise ValueError("Activity not found")

    update_data = data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise ValueError("No fields provided for update")

    if "destination_id" in update_data:
        destination = destinations_collection.find_one({
            "_id": _object_id(update_data["destination_id"])
        })

        if not destination:
            raise ValueError("Destination not found")

    if "price_unit" in update_data:
        if update_data["price_unit"] not in [
            "per_person",
            "per_group"
        ]:
            raise ValueError("Invalid price_unit")

    activities_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return get_activity(activity_id)


def delete_activity(activity_id: str):
    object_id = _object_id(activity_id)

    activity = activities_collection.find_one({
        "_id": object_id
    })

    if not activity:
        raise ValueError("Activity not found")

    activities_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": "deleted"
            }
        }
    )

    return {
        "activity_id": activity_id,
        "message": "Activity deleted successfully"
    }