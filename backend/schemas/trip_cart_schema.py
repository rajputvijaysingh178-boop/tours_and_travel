from pydantic import BaseModel, Field
from typing import List, Optional


class TripCartCreateSchema(BaseModel):
    package_id: str
    travel_date: str
    passenger_count: int = Field(
        ge=1,
        le=5
    )


class HotelSelectionSchema(BaseModel):
    hotel_id: str


class RoomSelectionSchema(BaseModel):
    room_id: str


class ActivitiesSelectionSchema(BaseModel):
    activity_ids: List[str] = []


class GuideSelectionSchema(BaseModel):
    guide_id: Optional[str] = None


class VehicleSelectionSchema(BaseModel):
    vehicle_id: Optional[str] = None


class PassengerSchema(BaseModel):
    name: str
    age: int = Field(gt=0)
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class PassengerDetailsSchema(BaseModel):
    passengers: List[PassengerSchema]


class ReviewSchema(BaseModel):
    confirmed: bool