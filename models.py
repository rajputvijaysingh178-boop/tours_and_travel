from pydantic import BaseModel


class Hotel(BaseModel):
    name: str
    location: str


class HotelRoom(BaseModel):
    room_number: int
    room_type: str
    price: float
    available: bool = True