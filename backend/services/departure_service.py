from database import departures_collection
from bson import ObjectId


def create_departure(departure_data):
    if departure_data.capacity <= 0:
        raise ValueError("Capacity must be greater than 0")

    departure = {
        "package_id": departure_data.package_id,
        "start_date": departure_data.start_date,
        "end_date": departure_data.end_date,
        "capacity": departure_data.capacity,
        "status": departure_data.status
    }

    result = departures_collection.insert_one(departure)

    return {
        "departure_id": str(result.inserted_id),
        "message": "Departure created successfully"
    }


def get_departures():
    departures = departures_collection.find()

    result = []

    for departure in departures:
        result.append({
            "departure_id": str(departure["_id"]),
            "package_id": departure["package_id"],
            "start_date": departure["start_date"],
            "end_date": departure["end_date"],
            "capacity": departure["capacity"],
            "status": departure["status"]
        })

    return result


def get_departure(departure_id: str):
    try:
        departure = departures_collection.find_one({
            "_id": ObjectId(departure_id)
        })
    except Exception:
        raise ValueError("Invalid departure id")

    if not departure:
        raise ValueError("Departure not found")

    return {
        "departure_id": str(departure["_id"]),
        "package_id": departure["package_id"],
        "start_date": departure["start_date"],
        "end_date": departure["end_date"],
        "capacity": departure["capacity"],
        "status": departure["status"]
    }