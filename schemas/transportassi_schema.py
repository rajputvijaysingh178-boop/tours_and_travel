from pydantic import BaseModel


class TransportAssignmentSchema(BaseModel):
    vehicle_id: str
    driver_id: str
    departure_id: str