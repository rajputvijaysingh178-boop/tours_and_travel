from database import guides_collection, tour_assignments_collection
from bson import ObjectId


def create_guide(guide_data):
    guide = {
        "name": guide_data.name,
        "phone": guide_data.phone,
        "languages": guide_data.languages,
        "destination_expertise": guide_data.destination_expertise,
        "availability": guide_data.availability,
        "workload": guide_data.workload
    }

    result = guides_collection.insert_one(guide)

    return {
        "guide_id": str(result.inserted_id),
        "message": "Guide created successfully"
    }


def get_available_guides():
    guides = guides_collection.find({
        "availability": True
    })

    result = []

    for guide in guides:
        result.append({
            "guide_id": str(guide["_id"]),
            "name": guide["name"],
            "phone": guide["phone"],
            "languages": guide["languages"],
            "destination_expertise": guide["destination_expertise"],
            "availability": guide["availability"],
            "workload": guide["workload"]
        })

    return result


def assign_guide(guide_id, departure_id):
    guide = guides_collection.find_one({
        "_id": ObjectId(guide_id)
    })

    if not guide:
        raise ValueError("Guide not found")

    if not guide["availability"]:
        raise ValueError("Guide is not available")

    assignment = {
        "guide_id": guide_id,
        "departure_id": departure_id
    }

    tour_assignments_collection.insert_one(assignment)

    guides_collection.update_one(
        {"_id": ObjectId(guide_id)},
        {"$set": {"availability": False}}
    )

    return {
        "message": "Guide assigned successfully",
        "guide_id": guide_id
    }


def get_guide_tours(guide_id):
    tours = tour_assignments_collection.find({
        "guide_id": guide_id
    })

    result = []

    for tour in tours:
        result.append({
            "assignment_id": str(tour["_id"]),
            "guide_id": tour["guide_id"],
            "departure_id": tour["departure_id"]
        })

    return result