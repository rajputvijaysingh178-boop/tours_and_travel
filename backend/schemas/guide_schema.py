from pydantic import BaseModel, Field
from typing import Optional, List


class GuideCreateSchema(BaseModel):
    destination_id: str
    name: str
    bio: str
    languages: List[str] = []
    experience_years: int = Field(ge=0)
    fee: float = Field(ge=0)
    images: List[str] = []
    status: str = "active"


class GuideUpdateSchema(BaseModel):
    destination_id: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    languages: Optional[List[str]] = None
    experience_years: Optional[int] = Field(
        default=None,
        ge=0
    )
    fee: Optional[float] = Field(
        default=None,
        ge=0
    )
    images: Optional[List[str]] = None
    status: Optional[str] = None


class GuideResponseSchema(BaseModel):
    guide_id: str
    destination_id: str
    name: str
    bio: str
    languages: List[str]
    experience_years: int
    fee: float
    images: List[str]
    status: str