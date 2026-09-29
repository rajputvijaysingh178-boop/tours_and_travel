from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityCreateSchema(BaseModel):
    destination_id: str
    name: str
    description: str
    duration_minutes: int = Field(gt=0)
    price: float = Field(ge=0)
    price_unit: str = "per_person"
    images: List[str] = []
    status: str = "active"


class ActivityUpdateSchema(BaseModel):
    destination_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(
        default=None,
        gt=0
    )
    price: Optional[float] = Field(
        default=None,
        ge=0
    )
    price_unit: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


class ActivityResponseSchema(BaseModel):
    activity_id: str
    destination_id: str
    name: str
    description: str
    duration_minutes: int
    price: float
    price_unit: str
    images: List[str]
    status: str