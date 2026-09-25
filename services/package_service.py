from datetime import datetime, timezone
from bson import ObjectId

from database import packages_collection


def create_package(package_data):
    package = {
        "name": package_data.name,
        "destination": package_data.destination,
        "description": package_data.description,
        "duration": package_data.duration,
        "base_price": package_data.base_price,
        "max_passengers": package_data.max_passengers,
        "start_date": package_data.start_date,
        "end_date": package_data.end_date,
        "status": "draft",
        "cancellation_policy": package_data.cancellation_policy,
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
    }

    if package_data.base_price <= 0:
        raise ValueError("Package price must be greater than 0")

    if package_data.max_passengers <= 0:
        raise ValueError("Maximum passengers must be greater than 0")

    result = packages_collection.insert_one(package)

    return {
        "package_id": str(result.inserted_id),
        "message": "Package created successfully"
    }


def get_packages():
    packages = packages_collection.find()

    result = []

    for package in packages:
        result.append({
            "package_id": str(package["_id"]),
            "name": package["name"],
            "destination": package["destination"],
            "description": package["description"],
            "duration": package["duration"],
            "base_price": package["base_price"],
            "max_passengers": package["max_passengers"],
            "start_date": package["start_date"],
            "end_date": package["end_date"],
            "status": package["status"],
            "cancellation_policy": package["cancellation_policy"]
        })

    return result


def get_package(package_id: str):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    return {
        "package_id": str(package["_id"]),
        "name": package["name"],
        "destination": package["destination"],
        "description": package["description"],
        "duration": package["duration"],
        "base_price": package["base_price"],
        "max_passengers": package["max_passengers"],
        "start_date": package["start_date"],
        "end_date": package["end_date"],
        "status": package["status"],
        "cancellation_policy": package["cancellation_policy"]
    }


def update_package(package_id: str, package_data):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    update_data = package_data.model_dump(exclude_none=True)

    if "base_price" in update_data:
        if update_data["base_price"] <= 0:
            raise ValueError("Package price must be greater than 0")

    if "max_passengers" in update_data:
        if update_data["max_passengers"] <= 0:
            raise ValueError(
                "Maximum passengers must be greater than 0"
            )

    if not update_data:
        raise ValueError("No fields provided for update")

    packages_collection.update_one(
        {"_id": ObjectId(package_id)},
        {"$set": update_data}
    )

    return get_package(package_id)


def publish_package(package_id: str):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    if package.get("status") == "published":
        raise ValueError("Package is already published")

    packages_collection.update_one(
        {"_id": ObjectId(package_id)},
        {
            "$set": {
                "status": "published"
            }
        }
    )

    return {
        "package_id": package_id,
        "message": "Package published successfully"
    }


def delete_package(package_id: str):
    try:
        package = packages_collection.find_one({
            "_id": ObjectId(package_id)
        })
    except Exception:
        raise ValueError("Invalid package id")

    if not package:
        raise ValueError("Package not found")

    packages_collection.delete_one({
        "_id": ObjectId(package_id)
    })

    return {
        "package_id": package_id,
        "message": "Package deleted successfully"
    }