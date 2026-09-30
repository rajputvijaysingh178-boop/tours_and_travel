from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any


class InvoiceResponseSchema(BaseModel):
    invoice_id: str
    booking_id: str
    invoice_number: str
    amount: float
    generated_at: datetime
    status: str
    customer_name: str | None = None
    package_name: str | None = None
    passengers: list[dict[str, Any]] = Field(default_factory=list)
    payment_status: str | None = None
    total_amount: float | None = None
    destination: str | None = None