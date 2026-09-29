from pydantic import BaseModel


class GuideCreateSchema(BaseModel):
    name: str
    phone: str
    languages: list[str]
    destination_expertise: list[str]
    availability: bool
    workload: int


class GuideUpdateSchema(BaseModel):
    name: str | None = None
    phone: str | None = None
    languages: list[str] | None = None
    destination_expertise: list[str] | None = None
    availability: bool | None = None
    workload: int | None = None


class GuideResponseSchema(BaseModel):
    guide_id: str
    name: str
    phone: str
    languages: list[str]
    destination_expertise: list[str]
    availability: bool
    workload: int    
    