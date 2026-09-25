from pydantic import BaseModel


# Hotel Model
class Hotel(BaseModel):
    name: str
    location: str


# Hotel Room Model
class HotelRoom(BaseModel):
    room_number: int
    room_type: str
    price: float
    available: bool = True


# Booking Model
class Booking(BaseModel):
    customer_id: int
    hotel_id: int
    room_number: int
    check_in: str
    check_out: str
    status: str = "confirmed"


# Payment Model
class Payment(BaseModel):
    booking_id: int
    amount: float
    payment_method: str
    payment_status: str = "pending"


# Refund Model
class Refund(BaseModel):
    payment_id: int
    amount: float
    reason: str
    refund_status: str = "pending"


# Customer Service Model
class CustomerService(BaseModel):
    customer_id: int
    issue: str
    description: str
    status: str = "open"


# Driver Service Model
class DriverService(BaseModel):
    customer_id: int
    driver_name: str
    vehicle_number: str
    pickup_location: str
    drop_location: str
    status: str = "available"
