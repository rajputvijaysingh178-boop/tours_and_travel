from database import transport_assignments_collection
from bson import ObjectId


def create_transport_assignment(
    vehicle_id,
    driver_id,
    departure_id
):
    assignment = {
        "vehicle_id": vehicle_id,
        "driver_id": driver_id,
        "departure_id": departure_id
    }

    result = transport_assignments_collection.insert_one(
        assignment
    )

    return {
        "assignment_id": str(result.inserted_id),
        "message": "Transport assigned successfully"
    }


def get_transport_assignment(assignment_id):
    assignment = transport_assignments_collection.find_one(
        {"_id": ObjectId(assignment_id)}
    )

    if not assignment:
        raise ValueError("Transport assignment not found")

    return {
        "assignment_id": str(assignment["_id"]),
        "vehicle_id": assignment["vehicle_id"],
        "driver_id": assignment["driver_id"],
        "departure_id": assignment["departure_id"]
    }