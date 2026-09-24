from pydantic import BaseModel


class PaymentCreateSchema(BaseModel):
    booking_id: str
    amount: float


class PaymentResponseSchema(BaseModel):
    payment_id: str
    booking_id: str
    payment_reference: str
    amount: float
    status: str
    payment_date: str