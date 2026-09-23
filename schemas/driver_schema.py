from pydantic import BaseModel


class DriverCreateSchema(BaseModel):
    name: str
    phone: str
    license_number: str
    availability: bool


class DriverUpdateSchema(BaseModel):
    name: str | None = None
    phone: str | None = None
    license_number: str | None = None
    availability: bool | None = None


class DriverResponseSchema(BaseModel):
    driver_id: str
    name: str
    phone: str
    license_number: str
    availability: bool