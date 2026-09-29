from datetime import datetime, timezone

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


def _serialize_package(package: dict):
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
        "start_date": package.get(
            "start_date",
            ""
        ),
        "end_date": package.get(
            "end_date",
            ""
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
        "start_date": package_data.start_date,
        "end_date": package_data.end_date,
        "status": "draft",
        "cancellation_policy": (
            package_data.cancellation_policy
        ),
        "images": package_data.images,
        "created_at": datetime.now(
            timezone.utc
        ).replace(tzinfo=None),
    }

    result = packages_collection.insert_one(
        package
    )

    return {
        "package_id": str(result.inserted_id),
        "message": "Package created successfully",
    }


def get_packages():
    packages = packages_collection.find()

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

    packages_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return get_package(package_id)


def publish_package(package_id: str):
    object_id = _get_object_id(package_id)

    package = packages_collection.find_one({
        "_id": object_id
    })

    if not package:
        raise ValueError(
            "Package not found"
        )

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

    packages_collection.delete_one({
        "_id": object_id
    })

    return {
        "package_id": package_id,
        "message": "Package deleted successfully",
    }