from pydantic import BaseModel


class CustomerUpdateSchema(BaseModel):
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None


class CustomerResponseSchema(BaseModel):
    id: str
    user_id: str
    phone: str
    address: str
    emergency_contact: str