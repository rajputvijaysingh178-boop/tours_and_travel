from fastapi import APIRouter

from schemas.driver_schema import DriverCreateSchema
from services.driver_service import create_driver
from services.driver_service import create_driver, get_drivers


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.post("")
def create_driver_route(
    data: DriverCreateSchema
):
    return create_driver(data)

@router.get("")
def get_drivers_route():
    return get_drivers()