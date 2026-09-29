from fastapi import APIRouter, HTTPException

from schemas.departure_schema import (
    DepartureCreateSchema,
    DepartureResponseSchema
)

from services.departure_service import (
    create_departure,
    get_departures,
    get_departure
)


router = APIRouter(
    prefix="/departures",
    tags=["Departures"]
)


@router.post("", response_model=dict)
def create_departure_route(
    data: DepartureCreateSchema
):
    return create_departure(data)


@router.get("", response_model=list[DepartureResponseSchema])
def get_departures_route():
    return get_departures()


@router.get("/{departure_id}", response_model=DepartureResponseSchema)
def get_departure_route(
    departure_id: str
):
    try:
        return get_departure(departure_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )