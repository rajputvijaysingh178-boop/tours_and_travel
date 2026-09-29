from pydantic import BaseModel, Field
from typing import Optional, List


class HotelCreateSchema(BaseModel):
    name: str
    destination_id: str
    description: str
    location: str
    contact_details: str
    star_rating: float = Field(ge=1, le=5)
    amenities: List[str] = []
    images: List[str] = []
    status: str = "draft"


class HotelResponseSchema(BaseModel):
    hotel_id: str
    name: str
    destination_id: str
    description: str
    location: str
    contact_details: str
    star_rating: float
    amenities: List[str]
    images: List[str]
    status: str


class HotelRoomCreateSchema(BaseModel):
    room_type: str
    description: str
    capacity: int = Field(gt=0, le=5)
    nightly_rate: float = Field(gt=0)
    images: List[str] = []
    total_units: int = Field(gt=0)
    status: str = "active"


class HotelRoomResponseSchema(BaseModel):
    room_id: str
    hotel_id: str
    room_type: str
    description: str
    capacity: int
    nightly_rate: float
    images: List[str]
    total_units: int
    status: str