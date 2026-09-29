from pydantic import BaseModel


class PassengerSchema(BaseModel):
    name: str
    age: int
    gender: str
    emergency_contact: str


class PassengerResponseSchema(BaseModel):
    id: str
    booking_id: str
    name: str
    age: int
    gender: str
    emergency_contact: str