from datetime import date, datetime, timedelta, timezone

from bson import ObjectId
from bson.errors import InvalidId

from database import (
    packages_collection,
    destinations_collection,
)


def _get_object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _parse_date(value, field_name: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a valid YYYY-MM-DD date")

    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid YYYY-MM-DD date")

    if parsed.isoformat() != value:
        raise ValueError(f"{field_name} must be a valid YYYY-MM-DD date")

    return parsed


def _availability_period(package: dict) -> tuple[date, date]:
    available_from = package.get("available_from") or package.get("start_date")
    available_until = package.get("available_until") or package.get("end_date")
    if not available_from or not available_until:
        raise ValueError("Package availability dates are not configured")

    start = _parse_date(available_from, "available_from")
    end = _parse_date(available_until, "available_until")
    if start > end:
        raise ValueError("available_from must be on or before available_until")

    duration = package.get("duration")
    if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
        raise ValueError("Package duration must be greater than 0")

    return start, end


def validate_package_travel_date(
    package: dict,
    travel_date: str,
) -> tuple[str, str]:
    if package.get("status") not in {"published", "active"}:
        raise ValueError("Package is not available")

    available_from, available_until = _availability_period(package)
    start = _parse_date(travel_date, "travel_date")
    end = start + timedelta(days=package["duration"] - 1)

    if start < datetime.now(timezone.utc).date():
        raise ValueError("Travel date cannot be in the past")
    if start < available_from:
        raise ValueError("Travel date is before package availability")
    if end > available_until:
        raise ValueError("The complete trip must fit within package availability")

    return start.isoformat(), end.isoformat()


def _serialize_package(package: dict):
    available_from = package.get("available_from") or package.get(
        "start_date",
        ""
    )
    available_until = package.get("available_until") or package.get(
        "end_date",
        ""
    )
    return {
        "package_id": str(package["_id"]),
        "name": package.get("name", ""),
        "destination_id": package.get(
            "destination_id"
        ),
        "description": package.get(
            "description",
            ""
        ),
        "duration": package.get(
            "duration",
            1
        ),
        "base_price": package.get(
            "base_price",
            0
        ),
        "max_passengers": package.get(
            "max_passengers",
            5
        ),
        "available_from": available_from,
        "available_until": available_until,
        "start_date": package.get(
            "start_date",
            available_from
        ),
        "end_date": package.get(
            "end_date",
            available_until
        ),
        "status": package.get(
            "status",
            "draft"
        ),
        "cancellation_policy": package.get(
            "cancellation_policy",
            ""
        ),
        "images": package.get(
            "images",
            []
        ),
    }


def create_package(package_data):
    destination_id = _get_object_id(
        package_data.destination_id
    )

    destination = destinations_collection.find_one({
        "_id": destination_id
    })

    if not destination:
        raise ValueError(
            "Destination not found"
        )

    if package_data.base_price <= 0:
        raise ValueError(
            "Package price must be greater than 0"
        )

    if not 1 <= package_data.max_passengers <= 5:
        raise ValueError(
            "Maximum passengers must be between 1 and 5"
        )

    package = {
        "name": package_data.name,
        "destination_id": package_data.destination_id,
        "description": package_data.description,
        "duration": package_data.duration,
        "base_price": package_data.base_price,
        "max_passengers": package_data.max_passengers,
        "available_from": package_data.available_from,
        "available_until": package_data.available_until,
        "status": package_data.status,
        "cancellation_policy": (
            package_data.cancellation_policy
        ),
        "images": package_data.images,
        "created_at": datetime.now(
            timezone.utc
        ).replace(tzinfo=None),
    }

    _availability_period(package)

    result = packages_collection.insert_one(
        package
    )

    return {
        "package_id": str(result.inserted_id),
        "message": "Package created successfully",
    }


def get_packages():
    packages = packages_collection.find({
        "status": {"$in": ["published", "active"]}
    })

    return [
        _serialize_package(package)
        for package in packages
    ]


def get_package(package_id: str):
    object_id = _get_object_id(package_id)

    package = packages_collection.find_one({
        "_id": object_id
    })

    if not package:
        raise ValueError(
            "Package not found"
        )

    if package.get("status") not in {"published", "active"}:
        raise ValueError("Package is not available")

    return _serialize_package(package)


def update_package(
    package_id: str,
    package_data
):
    object_id = _get_object_id(package_id)

    package = packages_collection.find_one({
        "_id": object_id
    })

    if not package:
        raise ValueError(
            "Package not found"
        )

    update_data = package_data.model_dump(
        exclude_none=True
    )

    if "start_date" in update_data:
        update_data.setdefault("available_from", update_data["start_date"])
        del update_data["start_date"]
    if "end_date" in update_data:
        update_data.setdefault("available_until", update_data["end_date"])
        del update_data["end_date"]

    if not update_data:
        raise ValueError(
            "No fields provided for update"
        )

    if "destination_id" in update_data:
        destination = destinations_collection.find_one({
            "_id": _get_object_id(
                update_data["destination_id"]
            )
        })

        if not destination:
            raise ValueError(
                "Destination not found"
            )

    if "max_passengers" in update_data:
        if not 1 <= update_data["max_passengers"] <= 5:
            raise ValueError(
                "Maximum passengers must be between 1 and 5"
            )

    updated_package = {**package, **update_data}
    if {
        "available_from",
        "available_until",
        "start_date",
        "end_date",
        "duration",
        "status",
    }.intersection(update_data):
        start_date, end_date = _availability_period(updated_package)
        update_data["available_from"] = start_date.isoformat()
        update_data["available_until"] = end_date.isoformat()

    packages_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    updated_package.update(update_data)
    return _serialize_package(updated_package)


def publish_package(package_id: str):
    object_id = _get_object_id(package_id)

    package = packages_collection.find_one({
        "_id": object_id
    })

    if not package:
        raise ValueError(
            "Package not found"
        )

    _availability_period(package)

    if package.get("status") == "published":
        raise ValueError(
            "Package is already published"
        )

    packages_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": "published"
            }
        }
    )

    return {
        "package_id": package_id,
        "message": "Package published successfully",
    }


def delete_package(package_id: str):
    object_id = _get_object_id(package_id)

    package = packages_collection.find_one({
        "_id": object_id
    })

    if not package:
        raise ValueError(
            "Package not found"
        )

    packages_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": "draft",
                "deactivated_at": datetime.now(
                    timezone.utc
                ).replace(tzinfo=None),
            }
        }
    )

    return {
        "package_id": package_id,
        "message": "Package deactivated successfully",
    }