from pydantic import BaseModel


class BookingCreateSchema(BaseModel):
    customer_id: str
    departure_id: str
    passenger_count: int


class BookingResponseSchema(BaseModel):
    booking_id: str
    customer_id: str
    departure_id: str
    passenger_count: int
    total_amount: float
    booking_status: str
    payment_status: str
    cancellation_details: str | None = None