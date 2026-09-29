from pymongo import MongoClient
from config import settings


_client: MongoClient | None = None


def connect() -> None:
    global _client

    if _client is not None:
        return

    if not settings.MONGO_URI:
        raise RuntimeError("MONGO_URI is not configured.")

    _client = MongoClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    _client.admin.command("ping")


def get_client() -> MongoClient:
    global _client

    if _client is None:
        connect()

    return _client


def get_database():
    return get_client()[settings.DB_NAME]


def get_collection(collection_name: str):
    return get_database()[collection_name]


def disconnect() -> None:
    global _client

    if _client is not None:
        _client.close()
        _client = None


# Existing collections
users_collection = get_collection("users")
customers_collection = get_collection("customers")
sessions_collection = get_collection("sessions")

vehicles_collection = get_collection("vehicles")
drivers_collection = get_collection("drivers")
guides_collection = get_collection("guides")
transport_assignments_collection = get_collection(
    "transport_assignments"
)
tour_assignments_collection = get_collection(
    "tour_assignments"
)

bookings_collection = get_collection("bookings")
passengers_collection = get_collection("passengers")
payments_collection = get_collection("payments")
invoices_collection = get_collection("invoices")
refunds_collection = get_collection("refunds")

packages_collection = get_collection("packages")
departures_collection = get_collection("departures")
itineraries_collection = get_collection("itineraries")

hotels_collection = get_collection("hotels")
hotel_rooms_collection = get_collection("hotel_rooms")


# New TravelEase collections
destinations_collection = get_collection("destinations")
activities_collection = get_collection("activities")
trip_carts_collection = get_collection("trip_carts")
inventory_holds_collection = get_collection("inventory_holds")
payment_orders_collection = get_collection("payment_orders")
vouchers_collection = get_collection("vouchers")