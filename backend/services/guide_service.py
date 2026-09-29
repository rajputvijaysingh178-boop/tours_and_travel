from bson import ObjectId
from bson.errors import InvalidId

from database import (
    guides_collection,
    destinations_collection,
)


def _object_id(value: str):
    try:
        return ObjectId(value)
    except InvalidId:
        raise ValueError("Invalid ID")


def _serialize(guide: dict):
    return {
        "guide_id": str(guide["_id"]),
        "destination_id": guide.get("destination_id"),
        "name": guide.get("name", ""),
        "bio": guide.get("bio", ""),
        "languages": guide.get("languages", []),
        "experience_years": guide.get(
            "experience_years", 0
        ),
        "fee": guide.get("fee", 0),
        "images": guide.get("images", []),
        "status": guide.get("status", "active"),
    }


def create_guide(data):
    destination = destinations_collection.find_one({
        "_id": _object_id(data.destination_id)
    })

    if not destination:
        raise ValueError("Destination not found")

    guide = {
        "destination_id": data.destination_id,
        "name": data.name,
        "bio": data.bio,
        "languages": data.languages,
        "experience_years": data.experience_years,
        "fee": data.fee,
        "images": data.images,
        "status": data.status,
    }

    result = guides_collection.insert_one(guide)

    return {
        "guide_id": str(result.inserted_id),
        "message": "Guide created successfully"
    }


def get_guides(destination_id=None):
    query = {
        "status": "active"
    }

    if destination_id:
        query["destination_id"] = destination_id

    guides = guides_collection.find(query)

    return [
        _serialize(guide)
        for guide in guides
    ]


def get_guide(guide_id: str):
    guide = guides_collection.find_one({
        "_id": _object_id(guide_id)
    })

    if not guide:
        raise ValueError("Guide not found")

    return _serialize(guide)


def update_guide(guide_id: str, data):
    object_id = _object_id(guide_id)

    guide = guides_collection.find_one({
        "_id": object_id
    })

    if not guide:
        raise ValueError("Guide not found")

    update_data = data.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise ValueError(
            "No fields provided for update"
        )

    if "destination_id" in update_data:
        destination = destinations_collection.find_one({
            "_id": _object_id(
                update_data["destination_id"]
            )
        })

        if not destination:
            raise ValueError(
                "Destination not found"
            )

    guides_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return get_guide(guide_id)


def delete_guide(guide_id: str):
    object_id = _object_id(guide_id)

    guide = guides_collection.find_one({
        "_id": object_id
    })

    if not guide:
        raise ValueError("Guide not found")

    guides_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "deleted"}}
    )

    return {
        "guide_id": guide_id,
        "message": "Guide deleted successfully"
    }