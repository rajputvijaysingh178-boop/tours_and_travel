from bson import ObjectId
from bson.errors import InvalidId


def parse_object_id(value: str, label: str = "id") -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise ValueError(f"Invalid {label}")


def as_id(document: dict, key: str = "id") -> dict:
    if not document:
        return document
    document[key] = str(document["_id"])
    return document
