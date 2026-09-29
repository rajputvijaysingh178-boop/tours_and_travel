from database import (
    packages_collection,
    hotel_rooms_collection,
    activities_collection,
    guides_collection,
    vehicles_collection,
)


def calculate_cart_price(cart: dict) -> dict:
    passenger_count = cart.get("passenger_count", 1)

    package_price = 0
    hotel_price = 0
    room_difference = 0
    activities_price = 0
    guide_price = 0
    vehicle_price = 0
    discount = 0

    package_id = cart.get("package_id")

    if package_id:
        package = packages_collection.find_one({
            "_id": __import__("bson").ObjectId(package_id)
        })

        if package:
            package_price = (
                package.get("base_price", 0)
                * passenger_count
            )

    room_id = cart.get("room_id")

    if room_id:
        room = hotel_rooms_collection.find_one({
            "_id": __import__("bson").ObjectId(room_id)
        })

        if room:
            nights = cart.get("nights", 1)
            hotel_price = (
                room.get("nightly_rate", 0)
                * nights
            )

    for activity_id in cart.get("activity_ids", []):
        activity = activities_collection.find_one({
            "_id": __import__("bson").ObjectId(activity_id)
        })

        if activity:
            price = activity.get("price", 0)
            unit = activity.get("price_unit", "per_person")

            if unit == "per_person":
                activities_price += price * passenger_count
            else:
                activities_price += price

    guide_id = cart.get("guide_id")

    if guide_id:
        guide = guides_collection.find_one({
            "_id": __import__("bson").ObjectId(guide_id)
        })

        if guide:
            guide_price = guide.get("fee", 0)

    vehicle_id = cart.get("vehicle_id")

    if vehicle_id:
        vehicle = vehicles_collection.find_one({
            "_id": __import__("bson").ObjectId(vehicle_id)
        })

        if vehicle:
            vehicle_price = vehicle.get("daily_fee", 0)

    subtotal = (
        package_price
        + hotel_price
        + room_difference
        + activities_price
        + guide_price
        + vehicle_price
    )

    tax = round(
        subtotal * 0.05,
        2
    )

    grand_total = subtotal + tax - discount

    return {
        "package_subtotal": package_price,
        "hotel_subtotal": hotel_price,
        "room_difference": room_difference,
        "activities_subtotal": activities_price,
        "guide_subtotal": guide_price,
        "vehicle_subtotal": vehicle_price,
        "discount": discount,
        "tax": tax,
        "subtotal": subtotal,
        "grand_total": grand_total,
    }