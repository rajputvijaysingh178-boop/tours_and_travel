from pydantic import BaseModel


class DepartureCreateSchema(BaseModel):
    package_id: str
    start_date: str
    end_date: str
    capacity: int
    status: str


class DepartureResponseSchema(BaseModel):
    departure_id: str
    package_id: str
    start_date: str
    end_date: str
    capacity: int
    status: str