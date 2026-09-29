from database import hotels_collection, hotel_rooms_collection
from bson import ObjectId


def create_hotel(hotel_data):
    hotel = {
        "name": hotel_data.name,
        "location": hotel_data.location,
        "contact_details": hotel_data.contact_details,
        "status": hotel_data.status
    }

    result = hotels_collection.insert_one(hotel)

    return {
        "hotel_id": str(result.inserted_id),
        "message": "Hotel created successfully"
    }


def get_hotels():
    hotels = hotels_collection.find()

    result = []

    for hotel in hotels:
        result.append({
            "hotel_id": str(hotel["_id"]),
            "name": hotel["name"],
            "location": hotel["location"],
            "contact_details": hotel["contact_details"],
            "status": hotel["status"]
        })

    return result


def add_room(hotel_id, room_data):
    hotel = hotels_collection.find_one({
        "_id": ObjectId(hotel_id)
    })

    if not hotel:
        raise ValueError("Hotel not found")

    room = {
        "hotel_id": hotel_id,
        "room_type": room_data.room_type,
        "capacity": room_data.capacity,
        "price": room_data.price,
        "available_from": room_data.available_from,
        "available_to": room_data.available_to
    }

    result = hotel_rooms_collection.insert_one(room)

    return {
        "room_id": str(result.inserted_id),
        "hotel_id": hotel_id,
        "message": "Room added successfully"
    }


def get_availability(hotel_id):
    hotel = hotels_collection.find_one({
        "_id": ObjectId(hotel_id)
    })

    if not hotel:
        raise ValueError("Hotel not found")

    rooms = hotel_rooms_collection.find({
        "hotel_id": hotel_id
    })

    result = []

    for room in rooms:
        result.append({
            "room_id": str(room["_id"]),
            "hotel_id": room["hotel_id"],
            "room_type": room["room_type"],
            "capacity": room["capacity"],
            "price": room["price"],
            "available_from": room["available_from"],
            "available_to": room["available_to"]
        })

    return result