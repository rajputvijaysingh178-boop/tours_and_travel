from fastapi import APIRouter, Depends, HTTPException

from schemas.destination_schema import (
    DestinationCreateSchema,
    DestinationUpdateSchema,
)

from services.destination_service import (
    create_destination,
    get_destinations,
    get_destination,
    update_destination,
    delete_destination,
)
from services.aut_dependency import get_admin_user


router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"]
)


@router.post("", dependencies=[Depends(get_admin_user)])
def create_destination_route(data: DestinationCreateSchema):
    try:
        return create_destination(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def get_destinations_route():
    return get_destinations()


@router.get("/{destination_id}")
def get_destination_route(destination_id: str):
    try:
        return get_destination(destination_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{destination_id}", dependencies=[Depends(get_admin_user)])
def update_destination_route(
    destination_id: str,
    data: DestinationUpdateSchema,
):
    try:
        return update_destination(destination_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{destination_id}", dependencies=[Depends(get_admin_user)])
def delete_destination_route(destination_id: str):
    try:
        return delete_destination(destination_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))