from fastapi import APIRouter

from schemas.vehicle_schema import VehicleCreateSchema

from services.vehicle_service import (
    create_vehicle,
    get_available_vehicles
)


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.post("")
def create_vehicle_route(
    data: VehicleCreateSchema
):
    return create_vehicle(data)


@router.get("/available")
def get_available_vehicles_route():
    return get_available_vehicles()

