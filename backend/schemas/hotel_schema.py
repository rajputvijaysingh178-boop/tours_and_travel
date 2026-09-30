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


class HotelUpdateSchema(BaseModel):
    name: Optional[str] = None
    destination_id: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    contact_details: Optional[str] = None
    star_rating: Optional[float] = Field(default=None, ge=1, le=5)
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


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


class HotelRoomUpdateSchema(BaseModel):
    room_type: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = Field(default=None, gt=0, le=5)
    nightly_rate: Optional[float] = Field(default=None, gt=0)
    images: Optional[List[str]] = None
    total_units: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = None


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