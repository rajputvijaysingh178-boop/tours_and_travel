from pydantic import BaseModel
from typing import Optional


class ItineraryCreateSchema(BaseModel):
    day_number: int
    destination: str
    activity: str
    start_time: str
    end_time: str
    inclusions: list[str] = []
    exclusions: list[str] = []


class ItineraryUpdateSchema(BaseModel):
    day_number: Optional[int] = None
    destination: Optional[str] = None
    activity: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    inclusions: Optional[list[str]] = None
    exclusions: Optional[list[str]] = None


class ItineraryResponseSchema(BaseModel):
    itinerary_id: str
    package_id: str
    day_number: int
    destination: str
    activity: str
    start_time: str
    end_time: str
    inclusions: list[str]
    exclusions: list[str]
    version: int