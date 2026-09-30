from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from bson import ObjectId
from bson.errors import InvalidId

import cloudinary
import cloudinary.uploader

from config import settings
from database import (
    activities_collection,
    bookings_collection,
    customers_collection,
    departures_collection,
    destinations_collection,
    guides_collection,
    hotel_rooms_collection,
    hotels_collection,
    invoices_collection,
    packages_collection,
    payments_collection,
    refunds_collection,
    users_collection,
    vehicles_collection,
)
from schemas.hotel_schema import HotelUpdateSchema, HotelRoomUpdateSchema
from services.aut_dependency import get_admin_user


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_admin_user)],
)

COLLECTIONS = {
    "destinations": (destinations_collection, "destination_id"),
    "packages": (packages_collection, "package_id"),
    "hotels": (hotels_collection, "hotel_id"),
    "rooms": (hotel_rooms_collection, "room_id"),
    "activities": (activities_collection, "activity_id"),
    "guides": (guides_collection, "guide_id"),
    "vehicles": (vehicles_collection, "vehicle_id"),
    "departures": (departures_collection, "departure_id"),
    "bookings": (bookings_collection, "booking_id"),
    "payments": (payments_collection, "payment_record_id"),
    "invoices": (invoices_collection, "invoice_record_id"),
    "refunds": (refunds_collection, "refund_record_id"),
}


def _object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid record ID")


def _clean(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return {
            key: _clean(item)
            for key, item in value.items()
            if key not in {"password_hash", "payment_signature"}
        }
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


def _related(collection, record_id: str | None):
    if not record_id:
        return None
    try:
        return collection.find_one({"_id": ObjectId(record_id)})
    except (InvalidId, TypeError):
        return None


def _serialize(collection_key: str, document: dict) -> dict:
    collection, id_field = COLLECTIONS[collection_key]
    result = _clean(document)
    result.pop("_id", None)
    result[id_field] = str(document["_id"])

    destination = _related(destinations_collection, document.get("destination_id"))
    if destination:
        result["destination_name"] = destination.get("name", "")
    if collection_key == "rooms":
        hotel = _related(hotels_collection, document.get("hotel_id"))
        result["hotel_name"] = hotel.get("name", "") if hotel else ""

    if collection_key == "bookings":
        customer = users_collection.find_one({"_id": _related_user_id(document.get("customer_id"))}) if document.get("customer_id") else None
        package = _related(packages_collection, document.get("package_id"))
        destination = _related(destinations_collection, document.get("destination_id"))
        hotel = _related(hotels_collection, document.get("hotel_id"))
        room = _related(hotel_rooms_collection, document.get("room_id"))
        guide = _related(guides_collection, document.get("guide_id"))
        vehicle = _related(vehicles_collection, document.get("vehicle_id"))
        result.update({
            "customer_name": customer.get("name", "") if customer else "",
            "customer_email": customer.get("email", "") if customer else "",
            "package_name": package.get("name", "") if package else "",
            "destination_name": destination.get("name", "") if destination else "",
            "hotel_name": hotel.get("name", "") if hotel else "",
            "room_type": room.get("room_type", "") if room else "",
            "guide_name": guide.get("name", "") if guide else "",
            "vehicle_name": vehicle.get("name", "") if vehicle else "",
        })
        activity_names = []
        for activity_id in document.get("activity_ids", []):
            activity = _related(activities_collection, activity_id)
            if activity:
                activity_names.append(activity.get("name", ""))
        result["activities"] = activity_names

    return result


def _related_user_id(user_id: str):
    try:
        return ObjectId(user_id)
    except (InvalidId, TypeError):
        return None


@router.get("/session")
def admin_session(current_user: dict = Depends(get_admin_user)):
    return {
        "id": str(current_user["_id"]),
        "name": current_user.get("name", "Administrator"),
        "email": current_user.get("email", ""),
        "role": current_user.get("role"),
    }


@router.get("/overview")
def admin_overview():
    paid_query = {"status": {"$in": ["paid", "completed"]}}
    revenue = sum(
        float(payment.get("amount", 0) or 0)
        for payment in payments_collection.find(paid_query, {"amount": 1})
    )
    return {
        "destinations": destinations_collection.count_documents({}),
        "packages": packages_collection.count_documents({}),
        "hotels": hotels_collection.count_documents({}),
        "customers": customers_collection.count_documents({}),
        "bookings": bookings_collection.count_documents({}),
        "revenue": revenue,
    }


@router.get("/records/{resource}")
def admin_records(
    resource: str,
    search: str = "",
    status: str | None = None,
    limit: int = 250,
):
    if resource == "customers":
        records = []
        for profile in customers_collection.find().sort("_id", -1).limit(min(limit, 500)):
            user = users_collection.find_one({"_id": _related_user_id(profile.get("user_id"))})
            record = _clean(profile)
            record.pop("_id", None)
            record["customer_id"] = str(profile["_id"])
            if user:
                record.update({
                    "name": user.get("name", ""),
                    "email": user.get("email", ""),
                    "created_at": user.get("created_at"),
                    "is_active": user.get("is_active", True),
                })
            records.append(record)
    else:
        if resource not in COLLECTIONS:
            raise HTTPException(status_code=404, detail="Unknown admin resource")
        collection, _ = COLLECTIONS[resource]
        query = {"status": status} if status else {}
        documents = collection.find(query).sort("_id", -1).limit(min(max(limit, 1), 500))
        records = [_serialize(resource, document) for document in documents]

    if search:
        needle = search.casefold()
        records = [
            record for record in records
            if needle in " ".join(str(value) for value in record.values()).casefold()
        ]
    return records


@router.patch("/hotels/{hotel_id}")
def update_hotel(hotel_id: str, data: HotelUpdateSchema):
    updates = data.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    if "destination_id" in updates and not destinations_collection.find_one({"_id": _object_id(updates["destination_id"])}):
        raise HTTPException(status_code=404, detail="Destination not found")
    result = hotels_collection.update_one({"_id": _object_id(hotel_id)}, {"$set": updates})
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return {"hotel_id": hotel_id, "message": "Hotel updated successfully"}


@router.patch("/rooms/{room_id}")
def update_room(room_id: str, data: HotelRoomUpdateSchema):
    updates = data.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    result = hotel_rooms_collection.update_one({"_id": _object_id(room_id)}, {"$set": updates})
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"room_id": room_id, "message": "Room updated successfully"}


@router.post("/images/upload")
def upload_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload an image file")
    if not all((settings.CLOUDINARY_CLOUD_NAME, settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET)):
        raise HTTPException(status_code=503, detail="Cloudinary is not configured")
    if len(file.file.read(10 * 1024 * 1024 + 1)) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Images must be 10 MB or smaller")
    file.file.seek(0)

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )
    try:
        uploaded = cloudinary.uploader.upload(
            file.file,
            folder="travelease/admin",
            resource_type="image",
        )
    except Exception as error:
        print(f"Cloudinary upload error: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=502,
            detail=f"Cloudinary upload failed: {type(error).__name__}"
        )
    return {
        "url": uploaded["secure_url"],
        "public_id": uploaded["public_id"],
    }


@router.get("/health")
def admin_health():
    cloudinary_fields = (
        "CLOUDINARY_CLOUD_NAME",
        "CLOUDINARY_API_KEY",
        "CLOUDINARY_API_SECRET",
    )
    missing_fields = [
        field for field in cloudinary_fields
        if not getattr(settings, field, "")
    ]
    return {
        "status": "ok",
        "cloudinary_configured": not missing_fields,
        "cloudinary_missing_fields": missing_fields,
    }
