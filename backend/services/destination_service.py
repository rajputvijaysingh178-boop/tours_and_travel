from bson import ObjectId
from bson.errors import InvalidId

from database import destinations_collection


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid destination ID")


def _serialize(destination):
    return {
        "destination_id": str(destination["_id"]),
        "name": destination.get("name", ""),
        "country": destination.get("country", ""),
        "state": destination.get("state", ""),
        "description": destination.get("description", ""),
        "images": destination.get("images", []),
        "status": destination.get("status", "active"),
    }


def create_destination(data):
    destination = {
        "name": data.name,
        "country": data.country,
        "state": data.state,
        "description": data.description,
        "images": data.images,
        "status": data.status,
    }

    result = destinations_collection.insert_one(destination)

    return {
        "destination_id": str(result.inserted_id),
        "message": "Destination created successfully",
    }


def get_destinations():
    destinations = destinations_collection.find()
    return [_serialize(destination) for destination in destinations]


def get_destination(destination_id: str):
    destination = destinations_collection.find_one(
        {"_id": _object_id(destination_id)}
    )

    if not destination:
        raise ValueError("Destination not found")

    return _serialize(destination)


def update_destination(destination_id: str, data):
    update_data = {
        key: value
        for key, value in data.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise ValueError("No fields to update")

    result = destinations_collection.update_one(
        {"_id": _object_id(destination_id)},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise ValueError("Destination not found")

    return {
        "destination_id": destination_id,
        "message": "Destination updated successfully",
    }


def delete_destination(destination_id: str):
    result = destinations_collection.delete_one(
        {"_id": _object_id(destination_id)}
    )

    if result.deleted_count == 0:
        raise ValueError("Destination not found")

    return {
        "message": "Destination deleted successfully"
    }