from pydantic import BaseModel


class HotelCreateSchema(BaseModel):
    name: str
    location: str
    contact_details: str
    status: str


class HotelResponseSchema(BaseModel):
    hotel_id: str
    name: str
    location: str
    contact_details: str
    status: str


class HotelRoomCreateSchema(BaseModel):
    room_type: str
    capacity: int
    price: float
    available_from: str
    available_to: str


class HotelRoomResponseSchema(BaseModel):
    room_id: str
    hotel_id: str
    room_type: str
    capacity: int
    price: float
    available_from: str
    available_to: str