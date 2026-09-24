from fastapi import APIRouter

from schemas.driver_schema import DriverCreateSchema
from services.driver_service import create_driver


router = APIRouter(prefix="/drivers",tags=["Drivers"])


@router.post("")
def create_driver_route(data: DriverCreateSchema):
    return create_driver(data)