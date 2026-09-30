from pydantic import BaseModel, Field
from typing import Optional


class PaymentVerificationSchema(BaseModel):
    payment_id: str
    payment_signature: Optional[str] = None


class CheckoutResponseSchema(BaseModel):
    cart_id: str
    payment_order_id: Optional[str] = None
    booking_id: Optional[str] = None
    invoice_id: Optional[str] = None
    voucher_id: Optional[str] = None
    amount: float
    status: str