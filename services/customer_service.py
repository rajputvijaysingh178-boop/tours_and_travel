from database import customers_collection, bookings_collection


def get_customer_profile(user_id):
    customer = customers_collection.find_one({"user_id": user_id})

    if not customer:
        raise ValueError("Customer profile not found")
    return {
        "id": str(customer["_id"]),
        "user_id": customer["user_id"],
        "phone": customer["phone"],
        "address": customer["address"],
        "emergency_contact": customer["emergency_contact"]
    }


def update_customer_profile(user_id, data):
    customer = customers_collection.find_one({"user_id": user_id})

    if not customer:
        raise ValueError("Customer profile not found")
    customers_collection.update_one(
        {"_id": customer["_id"]},
        {"$set": data})
    customer = customers_collection.find_one({
        "_id": customer["_id"]})
    return {
        "id": str(customer["_id"]),
        "user_id": customer["user_id"],
        "phone": customer["phone"],
        "address": customer["address"],
        "emergency_contact": customer["emergency_contact"]
    }


def get_customer_bookings(customer_id):
    customer = customers_collection.find_one({
        "user_id": customer_id})

    if not customer:
        raise ValueError("Customer not found")
    bookings = bookings_collection.find({
        "customer_id": customer_id})

    result = []

    for booking in bookings:
        booking["booking_id"] = str(booking["_id"])
        del booking["_id"]
        result.append(booking)

    return result