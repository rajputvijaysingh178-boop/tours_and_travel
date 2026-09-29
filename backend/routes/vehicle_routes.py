from fastapi import APIRouter, HTTPException

from schemas.vehicle_schema import (
    VehicleCreateSchema,
    VehicleUpdateSchema,
)

from services.vehicle_service import (
    create_vehicle,
    get_vehicles,
    get_vehicle,
    update_vehicle,
    delete_vehicle,
)


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.post("")
def create_vehicle_route(
    data: VehicleCreateSchema
):
    try:
        return create_vehicle(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_vehicles_route(
    destination_id: str | None = None
):
    return get_vehicles(destination_id)


@router.get("/{vehicle_id}")
def get_vehicle_route(vehicle_id: str):
    try:
        return get_vehicle(vehicle_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/{vehicle_id}")
def update_vehicle_route(
    vehicle_id: str,
    data: VehicleUpdateSchema
):
    try:
        return update_vehicle(
            vehicle_id,
            data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{vehicle_id}")
def delete_vehicle_route(
    vehicle_id: str
):
    try:
        return delete_vehicle(vehicle_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )