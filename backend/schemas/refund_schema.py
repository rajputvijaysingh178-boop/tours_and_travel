from pydantic import BaseModel


class RefundCreateSchema(BaseModel):
    refund_amount: float
    refund_percentage: float
    reason: str
class RefundResponseSchema(BaseModel):
    refund_id: str
    booking_id: str
    payment_id: str
    refund_amount: float
    refund_percentage: float
    reason: str
    status: str
    refund_date: str