from database import passengers_collection
from bson import ObjectId


def add_passenger(
    booking_id: str,
    passenger_data
):
    passenger = {
        "booking_id": booking_id,
        "name": passenger_data.name,
        "age": passenger_data.age,
        "gender": passenger_data.gender,
        "emergency_contact": passenger_data.emergency_contact
    }

    result = passengers_collection.insert_one(passenger)

    return {
        "passenger_id": str(result.inserted_id),
        "message": "Passenger added successfully"
    }


def get_passengers(booking_id: str):
    passengers = passengers_collection.find({
        "booking_id": booking_id
    })

    result = []

    for passenger in passengers:
        result.append({
            "passenger_id": str(passenger["_id"]),
            "booking_id": passenger["booking_id"],
            "name": passenger["name"],
            "age": passenger["age"],
            "gender": passenger["gender"],
            "emergency_contact": passenger["emergency_contact"]
        })

    return result