from bson import ObjectId
from bson.errors import InvalidId

from database import (
    hotels_collection,
    hotel_rooms_collection,
    destinations_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")

def create_hotel(hotel_data):

    destination = destinations_collection.find_one({
        "_id": _object_id(
            hotel_data.destination_id
        )
    })

    if not destination:
        raise ValueError(
            "Destination not found"
        )

    hotel = {
        "name": hotel_data.name,
        "destination_id": hotel_data.destination_id,
        "description": hotel_data.description,
        "location": hotel_data.location,
        "contact_details": hotel_data.contact_details,
        "star_rating": hotel_data.star_rating,
        "amenities": hotel_data.amenities,
        "images": hotel_data.images,
        "status": hotel_data.status,
    }

    result = hotels_collection.insert_one(hotel)

    return {
        "hotel_id": str(result.inserted_id),
        "message": "Hotel created successfully",
    }


def get_hotels(destination_id: str | None = None):
    query = {"status": "active"}

    if destination_id:
        query["destination_id"] = destination_id

    hotels = hotels_collection.find(query)
    result = []

    for hotel in hotels:
        result.append({
            "hotel_id": str(hotel["_id"]),
            "name": hotel.get("name", ""),
            "destination_id": hotel.get("destination_id"),
            "description": hotel.get("description", ""),
            "location": hotel.get("location", ""),
            "contact_details": hotel.get("contact_details", ""),
            "star_rating": hotel.get("star_rating", 0),
            "amenities": hotel.get("amenities", []),
            "images": hotel.get("images", []),
            "status": hotel.get("status", "active"),
        })

    return result


def add_room(hotel_id, room_data):

    hotel = hotels_collection.find_one({
        "_id": _object_id(hotel_id)
    })

    if not hotel:
        raise ValueError(
            "Hotel not found"
        )

    room = {
        "hotel_id": hotel_id,
        "room_type": room_data.room_type,
        "description": room_data.description,
        "capacity": room_data.capacity,
        "nightly_rate": room_data.nightly_rate,
        "images": room_data.images,
        "total_units": room_data.total_units,
        "status": room_data.status,
    }

    result = hotel_rooms_collection.insert_one(room)

    return {
        "room_id": str(result.inserted_id),
        "hotel_id": hotel_id,
        "message": "Room added successfully",
    }


def get_availability(hotel_id):

    hotel = hotels_collection.find_one({
        "_id": _object_id(hotel_id)
    })

    if not hotel:
        raise ValueError(
            "Hotel not found"
        )

    rooms = hotel_rooms_collection.find({
        "hotel_id": hotel_id,
        "status": "active",
    })

    result = []

    for room in rooms:
        result.append({
            "room_id": str(room["_id"]),
            "hotel_id": room["hotel_id"],
            "room_type": room.get(
                "room_type",
                ""
            ),
            "description": room.get(
                "description",
                ""
            ),
            "capacity": room.get(
                "capacity",
                1
            ),
            "nightly_rate": room.get(
                "nightly_rate",
                0
            ),
            "images": room.get(
                "images",
                []
            ),
            "total_units": room.get(
                "total_units",
                1
            ),
            "status": room.get(
                "status",
                "active"
            ),
        })

    return result