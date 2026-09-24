from pymongo import MongoClient

from config import settings


_client: MongoClient | None = None


def connect() -> None:
    global _client

    _client = MongoClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    _client.admin.command("ping")


def get_client() -> MongoClient:
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