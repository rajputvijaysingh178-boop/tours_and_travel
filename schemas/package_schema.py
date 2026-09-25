from pydantic import BaseModel
from typing import Optional


class PackageCreateSchema(BaseModel):
    name: str
    destination: str
    description: str
    duration: int
    base_price: float
    max_passengers: int
    start_date: str
    end_date: str
    cancellation_policy: str


class PackageUpdateSchema(BaseModel):
    name: Optional[str] = None
    destination: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    base_price: Optional[float] = None
    max_passengers: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    cancellation_policy: Optional[str] = None


class PackageResponseSchema(BaseModel):
    package_id: str
    name: str
    destination: str
    description: str
    duration: int
    base_price: float
    max_passengers: int
    start_date: str
    end_date: str
    status: str
    cancellation_policy: str