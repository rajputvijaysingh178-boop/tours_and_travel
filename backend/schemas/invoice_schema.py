from datetime import datetime
from pydantic import BaseModel


class InvoiceResponseSchema(BaseModel):
    invoice_id: str
    booking_id: str
    invoice_number: str
    amount: float
    generated_at: datetime
    status: str