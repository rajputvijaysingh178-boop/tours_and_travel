from bson import ObjectId

from database import (
    itineraries_collection,
    packages_collection
)


def create_itinerary(package_id: str, itinerary_data):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    itinerary = {
        "package_id": package_id,
        "day_number": itinerary_data.day_number,
        "destination": itinerary_data.destination,
        "activity": itinerary_data.activity,
        "start_time": itinerary_data.start_time,
        "end_time": itinerary_data.end_time,
        "inclusions": itinerary_data.inclusions,
        "exclusions": itinerary_data.exclusions,
        "version": 1
    }

    result = itineraries_collection.insert_one(itinerary)

    return {
        "itinerary_id": str(result.inserted_id),
        "message": "Itinerary created successfully"
    }


def get_package_itinerary(package_id: str):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    itineraries = itineraries_collection.find({
        "package_id": package_id
    }).sort("day_number", 1)

    result = []

    for itinerary in itineraries:
        result.append({
            "itinerary_id": str(itinerary["_id"]),
            "package_id": itinerary["package_id"],
            "day_number": itinerary["day_number"],
            "destination": itinerary["destination"],
            "activity": itinerary["activity"],
            "start_time": itinerary["start_time"],
            "end_time": itinerary["end_time"],
            "inclusions": itinerary["inclusions"],
            "exclusions": itinerary["exclusions"],
            "version": itinerary["version"]
        })

    return result


def update_itinerary(itinerary_id: str, itinerary_data):
    try:
        itinerary = itineraries_collection.find_one({
            "_id": ObjectId(itinerary_id)
        })
    except Exception:
        raise ValueError("Invalid itinerary id")

    if not itinerary:
        raise ValueError("Itinerary not found")

    update_data = itinerary_data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise ValueError("No fields provided for update")

    update_data["version"] = itinerary.get("version", 1) + 1

    itineraries_collection.update_one(
        {"_id": ObjectId(itinerary_id)},
        {"$set": update_data}
    )

    itinerary = itineraries_collection.find_one({
        "_id": ObjectId(itinerary_id)
    })

    return {
        "itinerary_id": str(itinerary["_id"]),
        "package_id": itinerary["package_id"],
        "day_number": itinerary["day_number"],
        "destination": itinerary["destination"],
        "activity": itinerary["activity"],
        "start_time": itinerary["start_time"],
        "end_time": itinerary["end_time"],
        "inclusions": itinerary["inclusions"],
        "exclusions": itinerary["exclusions"],
        "version": itinerary["version"]
    }


def delete_itinerary(itinerary_id: str):
    try:
        itinerary = itineraries_collection.find_one({
            "_id": ObjectId(itinerary_id)
        })
    except Exception:
        raise ValueError("Invalid itinerary id")

    if not itinerary:
        raise ValueError("Itinerary not found")

    itineraries_collection.delete_one({
        "_id": ObjectId(itinerary_id)
    })

    return {
        "itinerary_id": itinerary_id,
        "message": "Itinerary deleted successfully"
    }