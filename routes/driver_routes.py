from fastapi import APIRouter

<<<<<<< HEAD
=======
from schemas.driver_schema import DriverCreateSchema
from services.driver_service import create_driver


>>>>>>> origin/anil
router = APIRouter(prefix="/drivers",tags=["Drivers"])


@router.post("")
<<<<<<< HEAD
def create_driver():
    pass
=======
def create_driver_route(data: DriverCreateSchema):
    return create_driver(data)
>>>>>>> origin/anil
