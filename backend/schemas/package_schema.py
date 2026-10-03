from pydantic import BaseModel, Field
from typing import Optional, List


class PackageCreateSchema(BaseModel):
    name: str
    destination_id: str
    description: str
    duration: int = Field(gt=0)
    base_price: float = Field(gt=0)
    max_passengers: int = Field(default=5, ge=1, le=5)
    available_from: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    available_until: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    cancellation_policy: str
    images: List[str] = []
    status: str = "draft"


class PackageUpdateSchema(BaseModel):
    name: Optional[str] = None
    destination_id: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    base_price: Optional[float] = Field(default=None, gt=0)
    max_passengers: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )
    available_from: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    available_until: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    cancellation_policy: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None


class PackageResponseSchema(BaseModel):
    package_id: str
    name: str
    destination_id: str
    description: str
    duration: int
    base_price: float
    max_passengers: int
    available_from: str
    available_until: str
    start_date: str
    end_date: str
    status: str
    cancellation_policy: str
    images: List[str] = []