"""Idempotently seed six active hotels and rooms from existing destinations."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database import (  # noqa: E402
    destinations_collection,
    hotels_collection,
    hotel_rooms_collection,
)


PLACEHOLDER_IMAGES = [
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1200&q=80",
]

HOTELS = [
    ("Misty Grove Retreat", "Quiet hillside rooms with valley views.", "Tea Valley Road", 4.6),
    ("Cedar Peak Resort", "A calm base for early morning viewpoints.", "Top Station Road", 4.4),
    ("Fern & Falls Hotel", "Green, comfortable stays close to the falls.", "Munnar Bypass", 4.3),
    ("Cloudline House", "Warm hospitality and thoughtful local details.", "Old Market Lane", 4.7),
    ("The Cardamom Courtyard", "A garden stay surrounded by spice country.", "Chithirapuram", 4.5),
    ("Highland Hearth", "A relaxed retreat for slow travel and long views.", "Pallivasal", 4.2),
]


def seed() -> None:
    destinations = list(
        destinations_collection.find({"status": {"$ne": "deleted"}})
    )
    if not destinations:
        raise RuntimeError(
            "Create at least one destination before seeding hotels."
        )

    for index, (name, description, location, rating) in enumerate(HOTELS):
        destination_id = str(
            destinations[index % len(destinations)]["_id"]
        )
        hotel = {
            "name": name,
            "destination_id": destination_id,
            "description": description,
            "location": location,
            "contact_details": "+91 80000 00000",
            "star_rating": rating,
            "amenities": [
                "Wi-Fi",
                "Breakfast",
                "24-hour front desk",
                "Parking",
            ],
            "images": [PLACEHOLDER_IMAGES[index]],
            "status": "active",
        }
        result = hotels_collection.update_one(
            {"name": name, "destination_id": destination_id},
            {"$set": hotel},
            upsert=True,
        )
        hotel_id = result.upserted_id
        if hotel_id is None:
            hotel_id = hotels_collection.find_one(
                {"name": name, "destination_id": destination_id},
                {"_id": 1},
            )["_id"]

        for room_type, rate, capacity in (
            ("Deluxe Room", 4200, 2),
            ("Family Suite", 6800, 4),
        ):
            room = {
                "hotel_id": str(hotel_id),
                "room_type": room_type,
                "description": (
                    f"{room_type} at {name} with comfortable furnishings."
                ),
                "capacity": capacity,
                "nightly_rate": rate,
                "images": [PLACEHOLDER_IMAGES[index]],
                "total_units": 8,
                "status": "active",
            }
            hotel_rooms_collection.update_one(
                {
                    "hotel_id": str(hotel_id),
                    "room_type": room_type,
                },
                {"$set": room},
                upsert=True,
            )

    active_count = hotels_collection.count_documents(
        {"status": "active"}
    )
    print("Processed six active TravelEase hotels and two rooms per hotel.")
    print(f"Active hotels available: {active_count}")


if __name__ == "__main__":
    seed()
