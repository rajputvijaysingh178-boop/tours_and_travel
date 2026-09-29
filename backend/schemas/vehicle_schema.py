from pydantic import BaseModel, Field
from typing import Optional, List


class VehicleCreateSchema(BaseModel):
    name: str
    vehicle_type: str
    destination_id: Optional[str] = None
    capacity: int = Field(ge=1, le=50)
    daily_fee: float = Field(ge=0)
    images: List[str] = []
    status: str = "active"


class VehicleUpdateSchema(BaseModel):
    name: Optional[str] = None
    vehicle_type: Optional[str] = None
    destination_id: Optional[str] = None
    capacity: Optional[int] = Field(
        default=None,
        ge=1,
        le=50
    )
    daily_fee: Optional[float] = Field(
        default=None,
        ge=0
    )
    images: Optional[List[str]] = None
    status: Optional[str] = None


class VehicleResponseSchema(BaseModel):
    vehicle_id: str
    name: str
    vehicle_type: str
    destination_id: Optional[str]
    capacity: int
    daily_fee: float
    images: List[str]
    status: str