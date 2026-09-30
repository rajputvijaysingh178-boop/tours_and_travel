from pydantic import BaseModel
from typing import Optional, List


class DestinationCreateSchema(BaseModel):
    name: str
    country: str
    state: str
    description: str
    images: List[str] = []
    status: str = "active"


class DestinationUpdateSchema(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


class DestinationResponseSchema(BaseModel):
    destination_id: str
    name: str
    country: str
    state: str
    description: str
    images: List[str]
    status: str