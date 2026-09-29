from bson import ObjectId
from bson.errors import InvalidId

from database import (
    vehicles_collection,
    destinations_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _serialize(vehicle: dict):
    return {
        "vehicle_id": str(vehicle["_id"]),
        "name": vehicle.get("name", ""),
        "vehicle_type": vehicle.get("vehicle_type", ""),
        "destination_id": vehicle.get("destination_id"),
        "capacity": vehicle.get("capacity", 1),
        "daily_fee": vehicle.get("daily_fee", 0),
        "images": vehicle.get("images", []),
        "status": vehicle.get("status", "active"),
    }


def create_vehicle(data):
    if data.destination_id:
        destination = destinations_collection.find_one({
            "_id": _object_id(data.destination_id)
        })

        if not destination:
            raise ValueError("Destination not found")

    vehicle = {
        "name": data.name,
        "vehicle_type": data.vehicle_type,
        "destination_id": data.destination_id,
        "capacity": data.capacity,
        "daily_fee": data.daily_fee,
        "images": data.images,
        "status": data.status,
    }

    result = vehicles_collection.insert_one(vehicle)

    return {
        "vehicle_id": str(result.inserted_id),
        "message": "Vehicle created successfully"
    }


def get_vehicles(destination_id=None):
    query = {
        "status": "active"
    }

    if destination_id:
        query["destination_id"] = destination_id

    vehicles = vehicles_collection.find(query)

    return [
        _serialize(vehicle)
        for vehicle in vehicles
    ]


def get_vehicle(vehicle_id: str):
    vehicle = vehicles_collection.find_one({
        "_id": _object_id(vehicle_id)
    })

    if not vehicle:
        raise ValueError("Vehicle not found")

    return _serialize(vehicle)


def update_vehicle(vehicle_id: str, data):
    object_id = _object_id(vehicle_id)

    vehicle = vehicles_collection.find_one({
        "_id": object_id
    })

    if not vehicle:
        raise ValueError("Vehicle not found")

    update_data = data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise ValueError(
            "No fields provided for update"
        )

    if update_data.get("destination_id"):
        destination = destinations_collection.find_one({
            "_id": _object_id(
                update_data["destination_id"]
            )
        })

        if not destination:
            raise ValueError(
                "Destination not found"
            )

    vehicles_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return get_vehicle(vehicle_id)


def delete_vehicle(vehicle_id: str):
    object_id = _object_id(vehicle_id)

    vehicle = vehicles_collection.find_one({
        "_id": object_id
    })

    if not vehicle:
        raise ValueError("Vehicle not found")

    vehicles_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "deleted"}}
    )

    return {
        "vehicle_id": vehicle_id,
        "message": "Vehicle deleted successfully"
    }